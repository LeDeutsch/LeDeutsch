# 🏛️ ARCHITECTURE

Comment tout ça marche techniquement.

---

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub profile page (LeDeutsch/LeDeutsch)                  │
│  affiche README.md → qui affiche output/scene.svg           │
└─────────────────────────────────────────────────────────────┘
                             ▲
                             │ commit
                             │
┌─────────────────────────────────────────────────────────────┐
│  GitHub Action (cron 30min + on push)                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  scripts/generate_scene.py                            │  │
│  │  1. Lit l'heure                                        │  │
│  │  2. Fetch API GitHub → dernière activité de LeDeutsch │  │
│  │  3. Décide : pose, lumière, workload props            │  │
│  │  4. Compose les couches SVG                           │  │
│  │  5. Écrit output/scene.svg                            │  │
│  │  6. Met à jour le footer du README                    │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Structure des fichiers

```
LeDeutsch-profile/
├── README.md                    ← s'affiche sur le profil
├── .github/workflows/
│   └── update-scene.yml         ← l'automation
├── scripts/
│   └── generate_scene.py        ← le compositeur SVG
├── assets/                      ← les "briques" de la scène
│   ├── background/guild_hall.svg
│   ├── mascot/{idle,wave,sleep,code,drink,proud}.svg
│   ├── npcs/npc_layer.svg
│   └── props/{papers,coffee}.svg
├── output/
│   └── scene.svg                ← généré, référencé par le README
├── quests/                      ← les mini-jeux
│   ├── README.md                ← hub des quêtes
│   ├── nethardware/             ← 1 quête complète
│   └── {sao-utils, estiam-rfid, unity-hierarchy, lulu}/
└── docs/                        ← ce dossier
```

---

## Le système de couches SVG

Le SVG final (`output/scene.svg`) est **composé** de plusieurs fichiers `assets/*.svg` empilés dans cet ordre :

```
z=1  Background        ← toujours pareil (fond de guilde)
z=2  NPCs              ← hôtesses secondaires + aventuriers
z=3  Props dynamiques  ← papiers/tasses selon workload
z=4  Lumière overlay   ← rect coloré (bleu la nuit, orange au coucher)
z=5  Mascotte          ← toujours visible, une pose parmi 6
z=6  Bulle dialogue    ← texte contextualisé
```

Chaque asset est un `<g>` SVG (pas de `<svg>` wrapper). Le script les concatène dans un unique `<svg viewBox="0 0 1200 600">`.

**Pourquoi cette approche** : ajouter un nouvel élément dynamique = ajouter un fichier SVG + une ligne dans `generate_scene.py`. Zéro refonte.

---

## Les règles de décision

Dans `scripts/generate_scene.py`, trois fonctions décident de l'état de la scène :

### `pick_pose(hour, hours_since_push, msg)`

| Condition | Pose |
|---|---|
| `hour < 6` ou `hour >= 23` | `sleep` |
| `hours_since_push < 1` | `code` |
| `hours_since_push > 72` | `drink` |
| commit contient `fix`/`bug` | `proud` |
| commit contient `feat`/`add` | `wave` |
| sinon | `idle` |

### `pick_lighting(hour)`

| Plage horaire | Teinte | Opacité |
|---|---|---|
| 6h–9h | orange doux (aube) | 0.22 |
| 9h–17h | transparent (jour) | 0.00 |
| 17h–20h | orange chaud (crépuscule) | 0.28 |
| 20h–23h | violet-bleu (soirée) | 0.35 |
| 23h–6h | bleu nuit | 0.55 |

### Props dynamiques (workload)

Basé sur le nombre de commits push dans les dernières 24h :
- `>= 3` commits → couche `papers.svg` apparaît (docs entassés)
- `>= 6` commits → couche `coffee.svg` en plus (tasses vides = surmenage)

---

## Le pipeline de l'Action

Le workflow `.github/workflows/update-scene.yml` :

```yaml
Triggers:
  - schedule: every 30 min (cron)
  - push to main
  - workflow_dispatch (manuel)

Steps:
  1. checkout repo
  2. setup Python 3.11
  3. run scripts/generate_scene.py
       - lit assets/
       - fetch api.github.com/users/LeDeutsch/events/public
       - écrit output/scene.svg + met à jour README footer
  4. git commit + push si diff
```

**Permission requise** : le token par défaut `GITHUB_TOKEN` peut pousser si on a activé "Read and write permissions" (voir SETUP.md étape 3).

---

## Interactions & limites

### Ce qui est cliquable
- **Toute la scène** dans le README profil → lien vers `quests/README.md`
- Les liens texte du tableau des quêtes → chaque quête individuelle
- Dans chaque quête : les 4 choix → READMEs de "reveal"

### Ce qui NE peut PAS être fait dans un README GitHub
- ❌ JavaScript (script sanitizé)
- ❌ CSS custom (style sanitizé)
- ❌ Clics sur zones précises **d'une image SVG** (les `<a>` internes ne fonctionnent pas quand le SVG est chargé via `<img>` — et markdown `![](...)` le charge toujours via `<img>`)
- ❌ Hover / suivi de curseur
- ❌ Animations qui réagissent aux visiteurs

### Ce qui EST possible
- ✅ Régénération périodique de l'image (via Action)
- ✅ Image entière cliquable (via `[![](img)](link)`)
- ✅ Navigation via chaînes de README markdown
- ✅ Animations SMIL **bouclées** dans le SVG (breathing, blink) — mais on ne les utilise pas dans le MVP par simplicité de rendu et compatibilité camo

---

## Extensions possibles

Voir [ROADMAP.md](ROADMAP.md) pour la liste des évolutions prévues.

Les principales briques extensibles :
- **Ajouter une pose** : nouveau fichier `assets/mascot/xxx.svg` + une règle dans `pick_pose()`
- **Ajouter un prop dynamique** : nouveau fichier + une condition dans `build_scene()`
- **Ajouter une variante temporelle** (nuit vs jour très différentes) : dupliquer `guild_hall.svg` en `guild_hall_night.svg`, choisir dans `read_asset()`
- **Répliques IA** : appeler l'API Claude dans `pick_dialogue()` avec le message de commit + persona de l'hôtesse comme system prompt
