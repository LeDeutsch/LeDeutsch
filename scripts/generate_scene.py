#!/usr/bin/env python3
"""Compose the Guild Hall scene SVG from layered assets.

Called by the GitHub Action on a schedule and after each push.
The final scene = background + NPCs + dynamic props + lighting overlay + mascot,
where mascot pose, lighting, and props depend on the current time and the
owner's recent GitHub activity.
"""

from __future__ import annotations

import base64
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from functools import lru_cache
from io import BytesIO
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS = REPO_ROOT / "assets"
SCENE_DIR = ASSETS / "scene"
OUTPUT = REPO_ROOT / "output" / "scene.svg"
README = REPO_ROOT / "README.md"

GITHUB_USER = os.environ.get("GITHUB_USER", "LeDeutsch")
SCENE_WIDTH = 1920
SCENE_HEIGHT = 1080

MASCOT_DIR = ASSETS / "mascot" / "lucy"

# Available Lucy expressions (Lucy PNG filename without extension)
VALID_POSES = ("idle", "laugh", "happy", "neutral", "sad", "embarrassed")

BG_LAYERS = (
    "01_outside.png",
    "02_walls.png",
    "04_second_floor.png",
    "05_background_chairs.png",
    "03_lamps_flag.png",
    "06_counter_frame.png",
    "07_front_chair.png",
)

# FrontCounter renders BETWEEN Lucy body and Lucy arm overlay :
# body behind counter (hides her waist), arm on top of counter (resting).
FG_LAYERS = (
    "08_front_counter.png",
)

# Arm overlays extracted from Lucy PSD, rendered on top of the front counter
# so both arms (resting hand + raised hand at chin) stay visible over it.
MASCOT_ARM_OVERLAYS = (
    "lucy_arm_overlay.png",         # R hand 2 : the arm resting on counter
    "lucy_arm_raised_overlay.png",  # Right hand : the raised arm to chin
)

# Closed eyes overlay used for the blink animation (only on open-eye poses).
MASCOT_CLOSED_EYES_OVERLAY = "lucy_closed_eyes_overlay.png"
POSES_WITH_OPEN_EYES = frozenset({"idle", "laugh", "sad", "embarrassed"})

# Blush overlay (natural blush cropped from VARO's Head layer) used to pulse.
MASCOT_BLUSH_OVERLAY = "lucy_blush_overlay.png"

# Hair overlays for the sway animation.
MASCOT_HAIR_OVERLAYS = (
    ("lucy_hair_overlay.png", 1.2, 7.0),        # back hair : slower, wider sway
    ("lucy_front_hair_overlay.png", 0.9, 5.5),  # front hair : slightly faster, subtler
)

# Lucy PNG canvas is 5000x2750 with the character occupying bbox (1542, 62, 3608, 2697).
# We place her so she appears centered-horizontal, waist cut by front counter.
MASCOT_X, MASCOT_Y = 177, 230
MASCOT_W, MASCOT_H = 1520, 836

# Hair sway pivot (top of head in scene coords): head-top raw y=~200, head-center raw x=~2521
HAIR_PIVOT_X = int(MASCOT_X + 2521 * MASCOT_W / 5000)
HAIR_PIVOT_Y = int(MASCOT_Y + 220 * MASCOT_H / 2750)

# SMIL animation values.
BLINK_ANIM = (
    '<animate attributeName="opacity" '
    'values="0;0;0;0;0;0;0;0;0;1;0" dur="5s" repeatCount="indefinite"/>'
)
BLUSH_PULSE_ANIM = (
    '<animate attributeName="opacity" '
    'values="0.2;1;0.2" dur="3.5s" repeatCount="indefinite"/>'
)


def fetch_recent_activity(user: str) -> tuple[float | None, int, str]:
    """Return (hours_since_last_push, commits_last_24h, last_commit_message)."""
    url = f"https://api.github.com/users/{user}/events/public"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            events = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"[warn] GitHub API unreachable: {exc}", file=sys.stderr)
        return None, 0, ""

    push_events = [e for e in events if e.get("type") == "PushEvent"]
    if not push_events:
        return None, 0, ""

    latest = push_events[0]
    latest_ts = datetime.fromisoformat(latest["created_at"].replace("Z", "+00:00"))
    hours_since = (datetime.now(timezone.utc) - latest_ts).total_seconds() / 3600

    one_day_ago = datetime.now(timezone.utc).timestamp() - 86400
    commits_24h = 0
    for e in push_events:
        ts = datetime.fromisoformat(e["created_at"].replace("Z", "+00:00")).timestamp()
        if ts > one_day_ago:
            commits_24h += len(e["payload"].get("commits", []))

    commits = latest["payload"].get("commits") or []
    last_msg = commits[-1]["message"] if commits else ""
    return hours_since, commits_24h, last_msg


def pick_pose(hour: int, hours_since_push: float | None, msg: str) -> str:
    """Map current context to a Lucy expression (matches VALID_POSES filenames)."""
    if hour < 6 or hour >= 23:
        return "neutral"  # closed eyes calm, "sleeping" mode
    if hours_since_push is not None and hours_since_push > 72:
        return "sad"  # nobody has visited her in a while
    lower = msg.lower()
    if any(kw in lower for kw in ("revert", "hotfix")):
        return "embarrassed"  # oops
    if any(kw in lower for kw in ("fix", "bug")):
        return "happy"  # bug slain, closed happy eyes
    if any(kw in lower for kw in ("feat", "add")):
        return "laugh"  # new feature, cheerful open-mouth
    return "idle"


def pick_lighting(hour: int) -> dict:
    if 6 <= hour < 9:
        return {"color": "#ffcc80", "opacity": 0.22, "label": "dawn"}
    if 9 <= hour < 17:
        return {"color": "#ffffff", "opacity": 0.00, "label": "day"}
    if 17 <= hour < 20:
        return {"color": "#ff9966", "opacity": 0.28, "label": "dusk"}
    if 20 <= hour < 23:
        return {"color": "#5a4a8a", "opacity": 0.35, "label": "evening"}
    return {"color": "#1a1a4a", "opacity": 0.55, "label": "night"}


def pick_dialogue(pose: str, msg: str) -> str:
    snippets = {
        "idle": "Bienvenue, aventurier·ère. Quelle quête cherches-tu ?",
        "neutral": "Chut... reviens plus tard, la guilde est calme.",
        "sad": "Personne n'est passé depuis longtemps... reste un peu ?",
        "happy": "Une créature de bug vient d'être terrassée !",
        "laugh": "Ohé ! Une nouvelle fonctionnalité vient d'éclore.",
        "embarrassed": "Ah... ce n'était pas mon meilleur choix.",
    }
    text = snippets.get(pose, snippets["idle"])
    if pose in ("happy", "laugh", "embarrassed") and msg:
        first_line = msg.splitlines()[0][:60]
        text = f"{text} ({first_line})"
    return _xml_escape(text)


def _xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def read_asset(rel_path: str) -> str:
    path = ASSETS / rel_path
    if not path.exists():
        return f"<!-- missing asset: {rel_path} -->"
    return path.read_text(encoding="utf-8")


def build_dialogue_bubble(text: str) -> str:
    return f"""<g id="dialogue" transform="translate(1220, 380)">
  <rect x="0" y="0" width="600" height="100" rx="20" fill="#fffaf0" stroke="#5d3a26" stroke-width="4"/>
  <polygon points="50,100 80,100 30,140" fill="#fffaf0" stroke="#5d3a26" stroke-width="4"/>
  <polygon points="53,102 78,102 33,137" fill="#fffaf0"/>
  <text x="30" y="60" font-size="24" fill="#3a2820" font-family="Georgia, serif">{text}</text>
</g>"""


@lru_cache(maxsize=2)
def composite_layers(layer_files: tuple[str, ...]) -> str:
    """Alpha-composite PNG layers and return as base64 PNG data URI (cached)."""
    base = None
    for name in layer_files:
        path = SCENE_DIR / name
        img = Image.open(path).convert("RGBA")
        if base is None:
            base = Image.new("RGBA", img.size, (0, 0, 0, 0))
        base = Image.alpha_composite(base, img)

    buf = BytesIO()
    base.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


@lru_cache(maxsize=len(VALID_POSES))
def load_mascot_png(pose: str) -> str:
    """Load a Lucy expression PNG, downscale for web, return as base64 data URI."""
    path = MASCOT_DIR / f"lucy_{pose}.png"
    if not path.exists():
        print(f"[warn] missing mascot: {path}", file=sys.stderr)
        path = MASCOT_DIR / "lucy_idle.png"
    img = Image.open(path).convert("RGBA")

    # Source Lucy PNGs are 5000x2750 (~2MB each). We only render them
    # at ~1520 pixels wide in the scene, so 2x retina = 3040 max width.
    # Downscale keeps repo lean without visible quality loss.
    target_width = min(3040, img.width)
    if img.width > target_width:
        target_height = int(img.height * target_width / img.width)
        img = img.resize((target_width, target_height), Image.LANCZOS)

    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


@lru_cache(maxsize=8)
def load_arm_overlay_png(filename: str) -> str:
    """Load a Lucy arm overlay (extracted from PSD) and return as base64 data URI."""
    path = MASCOT_DIR / filename
    if not path.exists():
        return ""
    img = Image.open(path).convert("RGBA")
    target_width = min(3040, img.width)
    if img.width > target_width:
        target_height = int(img.height * target_width / img.width)
        img = img.resize((target_width, target_height), Image.LANCZOS)
    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def build_scene(pose: str, lighting: dict, workload: int, dialogue: str | None = None) -> str:
    bg_uri = composite_layers(BG_LAYERS)
    mascot_uri = load_mascot_png(pose)

    mascot_img = (
        f'<image href="{mascot_uri}" x="{MASCOT_X}" y="{MASCOT_Y}" '
        f'width="{MASCOT_W}" height="{MASCOT_H}"/>'
    )

    # Hair sway overlays applied ON TOP of body so their subtle rotation covers the
    # baked-in hair in the base image. Each hair layer has its own amplitude+period
    # so front and back don't move in perfect sync (feels more natural).
    hair_imgs = []
    for overlay_name, amp, dur in MASCOT_HAIR_OVERLAYS:
        hair_uri = load_arm_overlay_png(overlay_name)
        if hair_uri:
            sway = (
                f'<animateTransform attributeName="transform" type="rotate" '
                f'values="-{amp} {HAIR_PIVOT_X} {HAIR_PIVOT_Y};'
                f'{amp} {HAIR_PIVOT_X} {HAIR_PIVOT_Y};'
                f'-{amp} {HAIR_PIVOT_X} {HAIR_PIVOT_Y}" '
                f'dur="{dur}s" repeatCount="indefinite"/>'
            )
            hair_imgs.append(
                f'<image href="{hair_uri}" x="{MASCOT_X}" y="{MASCOT_Y}" '
                f'width="{MASCOT_W}" height="{MASCOT_H}">{sway}</image>'
            )
    hair_img = "\n  ".join(hair_imgs)

    fg_img = ""
    if FG_LAYERS:
        fg_uri = composite_layers(FG_LAYERS)
        fg_img = (
            f'<image href="{fg_uri}" x="0" y="0" '
            f'width="{SCENE_WIDTH}" height="{SCENE_HEIGHT}"/>'
        )

    arm_imgs = []
    for overlay_name in MASCOT_ARM_OVERLAYS:
        arm_uri = load_arm_overlay_png(overlay_name)
        if arm_uri:
            arm_imgs.append(
                f'<image href="{arm_uri}" x="{MASCOT_X}" y="{MASCOT_Y}" '
                f'width="{MASCOT_W}" height="{MASCOT_H}"/>'
            )
    arm_img = "\n  ".join(arm_imgs)

    # Blink cycle only applies when the base pose has open eyes.
    blink_img = ""
    if pose in POSES_WITH_OPEN_EYES:
        blink_uri = load_arm_overlay_png(MASCOT_CLOSED_EYES_OVERLAY)
        if blink_uri:
            blink_img = (
                f'<image href="{blink_uri}" x="{MASCOT_X}" y="{MASCOT_Y}" '
                f'width="{MASCOT_W}" height="{MASCOT_H}" opacity="0">'
                f'{BLINK_ANIM}</image>'
            )

    # Pulsing blush using the natural blush cropped from VARO's Head layer.
    # The overlay adds MORE saturation on top of Lucy's baked-in blush.
    blush_img = ""
    blush_uri = load_arm_overlay_png(MASCOT_BLUSH_OVERLAY)
    if blush_uri:
        blush_img = (
            f'<image href="{blush_uri}" x="{MASCOT_X}" y="{MASCOT_Y}" '
            f'width="{MASCOT_W}" height="{MASCOT_H}" opacity="0">'
            f'{BLUSH_PULSE_ANIM}</image>'
        )

    # Zzz drifting up for sleep mode (neutral pose = closed eyes calm).
    zzz_group = ""
    if pose == "neutral":
        zzz_x = int(MASCOT_X + 3200 * MASCOT_W / 5000)
        zzz_y_base = int(MASCOT_Y + 300 * MASCOT_H / 2750)
        zzz_group = f'''<g font-family="Georgia, serif" font-weight="bold" fill="#4a6a8a">
  <text x="{zzz_x}" y="{zzz_y_base}" font-size="42" opacity="0">Z
    <animate attributeName="opacity" values="0;1;0" dur="3s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0,0;0,-40" dur="3s" repeatCount="indefinite"/>
  </text>
  <text x="{zzz_x + 40}" y="{zzz_y_base - 40}" font-size="52" opacity="0">Z
    <animate attributeName="opacity" values="0;1;0" dur="3s" begin="1s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0,0;0,-40" dur="3s" begin="1s" repeatCount="indefinite"/>
  </text>
  <text x="{zzz_x + 80}" y="{zzz_y_base - 80}" font-size="62" opacity="0">Z
    <animate attributeName="opacity" values="0;1;0" dur="3s" begin="2s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0,0;0,-40" dur="3s" begin="2s" repeatCount="indefinite"/>
  </text>
</g>'''

    lighting_rect = (
        f'<rect x="0" y="0" width="{SCENE_WIDTH}" height="{SCENE_HEIGHT}" '
        f'fill="{lighting["color"]}" opacity="{lighting["opacity"]}"/>'
    )

    bubble = build_dialogue_bubble(dialogue) if dialogue else ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SCENE_WIDTH} {SCENE_HEIGHT}" font-family="'Segoe UI', Verdana, sans-serif">
  <title>Guilde des Aventuriers de LeDeutsch - {lighting['label']} - {pose}</title>
  <image href="{bg_uri}" x="0" y="0" width="{SCENE_WIDTH}" height="{SCENE_HEIGHT}"/>
  {mascot_img}
  {hair_img}
  {blink_img}
  {blush_img}
  {fg_img}
  {arm_img}
  {zzz_group}
  {lighting_rect}
  {bubble}
</svg>
"""


def update_readme_footer(pose: str, lighting_label: str, commits_24h: int) -> None:
    if not README.exists():
        return
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    marker_start = "<!-- SCENE-META:START -->"
    marker_end = "<!-- SCENE-META:END -->"
    content = README.read_text(encoding="utf-8")
    new_block = (
        f"{marker_start}\n"
        f"<sub>Scène : **{pose}** · lumière : **{lighting_label}** · "
        f"commits 24h : **{commits_24h}** · maj : {now}</sub>\n"
        f"{marker_end}"
    )
    if marker_start in content and marker_end in content:
        pre, rest = content.split(marker_start, 1)
        _, post = rest.split(marker_end, 1)
        README.write_text(pre + new_block + post, encoding="utf-8")
    else:
        README.write_text(content.rstrip() + "\n\n" + new_block + "\n", encoding="utf-8")


def main() -> None:
    hour = datetime.now().hour
    hours_since, commits_24h, msg = fetch_recent_activity(GITHUB_USER)
    lighting = pick_lighting(hour)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    dynamic_pose = pick_pose(hour, hours_since, msg)
    dynamic_dialogue = pick_dialogue(dynamic_pose, msg)
    main_svg = build_scene(dynamic_pose, lighting, commits_24h, dynamic_dialogue)
    OUTPUT.write_text(main_svg, encoding="utf-8")

    for pose in VALID_POSES:
        variant_svg = build_scene(pose, lighting, commits_24h, dialogue=None)
        variant_path = OUTPUT.parent / f"scene_{pose}.svg"
        variant_path.write_text(variant_svg, encoding="utf-8")

    update_readme_footer(dynamic_pose, lighting["label"], commits_24h)

    print(
        f"scene: main pose={dynamic_pose} lighting={lighting['label']} "
        f"hour={hour} commits_24h={commits_24h} + {len(VALID_POSES)} variants"
    )


if __name__ == "__main__":
    main()
