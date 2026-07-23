#!/usr/bin/env python3
"""Compose the Guild Hall scene SVG from layered assets.

Called by the GitHub Action on a schedule and after each push.
The final scene = background + NPCs + dynamic props + lighting overlay + mascot,
where mascot pose, lighting, and props depend on the current time and the
owner's recent GitHub activity.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS = REPO_ROOT / "assets"
OUTPUT = REPO_ROOT / "output" / "scene.svg"
README = REPO_ROOT / "README.md"

GITHUB_USER = os.environ.get("GITHUB_USER", "LeDeutsch")
SCENE_WIDTH = 1200
SCENE_HEIGHT = 600

VALID_POSES = {"idle", "code", "sleep", "drink", "proud", "wave"}


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
    if hour < 6 or hour >= 23:
        return "sleep"
    if hours_since_push is not None and hours_since_push < 1:
        return "code"
    if hours_since_push is not None and hours_since_push > 72:
        return "drink"
    lower = msg.lower()
    if any(kw in lower for kw in ("fix", "bug")):
        return "proud"
    if any(kw in lower for kw in ("feat", "add")):
        return "wave"
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
        "code": "Chut... il est en pleine session. Une nouvelle quête arrive.",
        "sleep": "Zzz... reviens à l'aube, brave âme.",
        "drink": "Aucun signe de lui depuis des jours... du thé ?",
        "proud": "Une créature de bug vient d'être terrassée !",
        "wave": "Ohé ! Une nouvelle fonctionnalité vient d'éclore.",
    }
    text = snippets.get(pose, snippets["idle"])
    if pose in ("code", "proud", "wave") and msg:
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
    return f"""<g id="dialogue" transform="translate(680, 210)">
  <rect x="0" y="0" width="380" height="70" rx="14" fill="#fffaf0" stroke="#5d3a26" stroke-width="3"/>
  <polygon points="30,70 45,70 20,95" fill="#fffaf0" stroke="#5d3a26" stroke-width="3"/>
  <polygon points="32,71 43,71 22,93" fill="#fffaf0"/>
  <text x="20" y="40" font-size="16" fill="#3a2820" font-family="Georgia, serif">{text}</text>
</g>"""


def build_scene(pose: str, lighting: dict, workload: int, dialogue: str) -> str:
    background = read_asset("background/guild_hall.svg")
    npcs = read_asset("npcs/npc_layer.svg")
    mascot = read_asset(f"mascot/{pose}.svg")

    props = ""
    if workload >= 3:
        props += read_asset("props/papers.svg")
    if workload >= 6:
        props += read_asset("props/coffee.svg")

    lighting_rect = (
        f'<rect x="0" y="0" width="{SCENE_WIDTH}" height="{SCENE_HEIGHT}" '
        f'fill="{lighting["color"]}" opacity="{lighting["opacity"]}"/>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SCENE_WIDTH} {SCENE_HEIGHT}" font-family="'Segoe UI', Verdana, sans-serif">
  <title>Guilde des Aventuriers de LeDeutsch — {lighting['label']} — {pose}</title>
  {background}
  {npcs}
  {props}
  {lighting_rect}
  {mascot}
  {build_dialogue_bubble(dialogue)}
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
        f"<sub>🌙 Scène : **{pose}** · lumière : **{lighting_label}** · "
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
    pose = pick_pose(hour, hours_since, msg)
    lighting = pick_lighting(hour)
    dialogue = pick_dialogue(pose, msg)

    svg = build_scene(pose, lighting, commits_24h, dialogue)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg, encoding="utf-8")

    update_readme_footer(pose, lighting["label"], commits_24h)

    print(
        f"scene: pose={pose} lighting={lighting['label']} "
        f"hour={hour} commits_24h={commits_24h} hours_since_push={hours_since}"
    )


if __name__ == "__main__":
    main()
