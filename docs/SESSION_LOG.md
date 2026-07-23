# 📝 Session Log — Guild Hall Project

Journal de bord des sessions de travail sur le profil GitHub. À lire en début de chaque nouvelle session pour reprendre le contexte.

---

## 🗓️ Session 1 — 2026-07-23 (MVP livré)

### 🎯 Le concept qu'on a arrêté

**"LeDeutsch's Guild Hall"** — le profil GitHub est mis en scène comme une **guilde d'aventuriers** à la JRPG/anime.

- **Fond fixe** : intérieur de salle de guilde vue de face (comptoir central en U, comptoirs sur les côtés, tableau des quêtes au mur, fenêtre, torches)
- **Mascotte au premier plan** : l'**hôtesse** de guilde, en 2D, face au visiteur derrière son comptoir central
- **NPCs de fond** : autres hôtesses sur les côtés, aventuriers de passage → salle vivante
- **Ambiance dynamique** : lumière change selon l'heure (aube/jour/crépuscule/nuit), props apparaissent selon la charge de travail
- **Interaction visiteur** : cliquer la scène → menu des quêtes → chaque quête est un **mini-jeu qui présente un projet réel** (nethardware-monitor, SAO-Utils-Patch-lang-fr, Estiam-RFID, custom-hierarchy-Unity, LULU)
- **Fil rouge** : le visiteur devient un aventurier qui accomplit des quêtes → système de progression (0/5 → 5/5 → quête cachée débloquée)

### 🧠 Décisions clés et pourquoi

| Décision | Pourquoi |
|---|---|
| **2D** (pas 3D) | Cohérent avec le style arcade/JRPG, moins d'effort par pose, SVG scalable, correspond à l'esthétique anime de l'avatar Ichigo |
| **Composition en couches SVG** | Extensibilité : ajouter un élément dynamique = ajouter un fichier + une ligne dans le générateur. Pas de refonte |
| **Régénération périodique (cron 30min + on push)** | Compromis entre fraîcheur et coût. La vraie "vie temps réel" style Wallpaper Engine est impossible sur GitHub README (pas de JS) |
| **Toute la scène = 1 lien cliquable** | Les `<a>` internes de SVG ne marchent pas quand le SVG est chargé via `<img>` (ce que fait toujours markdown). Fallback : image entière wrappée dans un lien markdown |
| **Mini-jeux = navigation entre READMEs** | Seule interactivité possible dans un README GitHub. Le visiteur "joue" en cliquant sur des liens qui révèlent des READMEs successifs |
| **Placeholders SVG moches d'abord** | Valider la MÉCANIQUE avant d'investir dans les assets. Le rendu est "greybox" comme un proto de jeu vidéo |
| **Repo cible = `LeDeutsch/LeDeutsch`** | Repo spécial GitHub dont le README s'affiche sur la page de profil. Force-push OK, le contenu précédent était juste le template "Hi there 👋" par défaut (backup dans `../LeDeutsch-backup/`) |

### ✅ Ce qui est en place

- Structure complète du repo (voir `docs/ARCHITECTURE.md`)
- Générateur Python `scripts/generate_scene.py` avec 3 fonctions clés : `pick_pose()`, `pick_lighting()`, `pick_dialogue()`
- GitHub Action `.github/workflows/update-scene.yml` qui régénère toutes les 30 min et à chaque push
- 6 poses de mascotte : `idle`, `wave`, `sleep`, `code`, `drink`, `proud` (placeholders SVG)
- Fond de guilde placeholder
- 4 NPCs de fond
- 2 props dynamiques (`papers`, `coffee`) qui apparaissent quand la charge de travail est haute
- Overlay lumière avec 5 variantes (aube/jour/crépuscule/soirée/nuit)
- Bulle de dialogue contextualisée
- README profil + hub de quêtes
- **1 quête complète** : `quests/nethardware/` (README + 4 reveals, dont 1 bon et 3 mauvais)
- **4 quêtes placeholder** : `sao-utils`, `estiam-rfid`, `unity-hierarchy`, `lulu`
- Documentation : `SETUP.md`, `ASSETS.md`, `ARCHITECTURE.md`, `ROADMAP.md`

### 🚀 État du déploiement (fin de session 1)

- [x] Backup du précédent README (`../LeDeutsch-backup/`)
- [x] Push force sur `LeDeutsch/LeDeutsch`
- [x] Workflow permissions activées (Read and write)
- [x] Premier run manuel de l'Action déclenché avec succès
- [x] Profil vérifié — **fonctionne parfaitement** ✅

### 🎨 État des assets

Tous les SVG dans `assets/` sont **des placeholders volontairement moches** faits pour valider la mécanique. À remplacer par de vrais assets — voir `docs/ASSETS.md`.

**Options discutées (par ordre de reco pour la suite)** :

1. **Vroid Studio** (gratuit, 2-3h d'apprentissage) — modéliser l'hôtesse en 3D → rendre des poses 2D cohérentes. Fond IA one-shot (Midjourney) à côté. **Coût : 0-15€.**
2. **Commission Skeb ou Fiverr** — character sheet pro avec 6 poses. Coût 50-200€. Meilleur rendu artistique.
3. **Live2D** — dessin unique animé, si on a l'illustration de base.
4. **Stable Diffusion + LoRA** — si l'user est technique.
5. **Packs itch.io** — dernier recours, style pas 100% perso.

### ❓ Décisions à prendre (prochaine session)

- **Nom de la guilde** — actuellement "Guilde des Aventuriers de LeDeutsch" (placeholder plat)
- **Nom de l'hôtesse** — actuellement anonyme. Suggestions à brainstormer : Skadi, Iris, Yuna, Reika, Elin…
- **Voie assets choisie** — Vroid (gratuit, à faire soi-même) OU commission (payant, délai) ?
- **Priorité quêtes** — laquelle transformer en mini-jeu réel en premier après nethardware ? (SAO-Utils est le plus narratif/original ; Estiam-RFID le plus démonstratif technique)

### 📅 Agenda prochaine session (priorité recommandée)

1. **Produire les assets réels** (~1 weekend en Vroid, ~2 semaines si commission)
   - Fond de guilde
   - Mascotte 6 poses
   - NPCs 2-3 silhouettes plus soignées
2. **Nommer** la guilde et l'hôtesse (à faire par Ludwig entre les sessions, cool)
3. **Compléter 1 ou 2 quêtes** au format mini-jeu vraiment jouable
4. **Optionnel** — brancher l'API Claude (Haiku, très pas cher) pour que la mascotte génère ses dialogues à partir du vrai commit message + un system prompt "persona"

### 🧩 Points techniques à retenir pour la reprise

- Le repo profil est `LeDeutsch/LeDeutsch` sur GitHub, cloné en local dans `c:/Users/lespe/OneDrive/Bureau/LeDeutsch-profile/`
- Le workflow tourne toutes les 30 min (cron) ET à chaque push
- Le token GitHub qu'on a utilisé pour le push a les scopes `repo` + `workflow`
- Le nethardware-monitor de Ludwig est un projet **totalement séparé** — les deux n'ont aucun lien de code, juste un lien narratif (nethardware-monitor est présenté comme une quête dans le profil)
- Ludwig (l'user) est étudiant à ESTIAM, à Paris, avatar anime (Ichigo de Bleach), aime l'esthétique JRPG/anime type Miku wallpaper

### 📂 Fichiers clés à ouvrir en début de reprise

- Ce fichier
- `docs/ROADMAP.md` — pour voir les phases planifiées
- `docs/ASSETS.md` — pour la voie assets choisie
- `scripts/generate_scene.py` — la logique centrale, à étendre pour toute nouvelle règle
- `assets/` — les placeholders à remplacer

---

## 🗓️ Session 2 — 2026-07-23 (dialog tree + scène vivante)

### 🎯 Décisions prises

1. **Paradigme d'interaction choisi : Option A (navigation entre fichiers)** — après avoir exploré les 3 options possibles (A = nav vers file viewer, B = `<details>` in-place, C = issues+Action), Ludwig a choisi de garder A. Raison : *"le profil doit être clean en présentation, si quelqu'un veut jouer il navigue dans les files, tant pis pour la chrome moche"*. Décision pragmatique.
2. **Focus sur la vivacité de la scène** au lieu de chercher plus d'interactivité — les animations SMIL sont l'axe prioritaire.

### ✅ Ce qui a été ajouté

- **Arbre de dialogue** (dossier `dialog/`) :
  - `greet.md` → `greet_name.md`
  - `rest.md` → `rest_bye.md` OU `wake.md`
  - Le README profil a maintenant 3 boutons : 👋 Saluer / 📜 Quêtes / 💤 Repos
- **Générateur refactoré** pour produire **7 scènes** au lieu d'1 : `scene.svg` (dynamique, avec bulle) + 6 variantes `scene_<pose>.svg` (sans bulle, pour les pages de dialogue) — tout ça avec la même lumière/props pour cohérence
- **Animations SMIL** dans les SVG (visibles en permanence, aucun clic requis) :
  - 🫁 Respiration de la mascotte (Y translate ±3px sur 4s, 6s pour sleep)
  - 👁️ Clignements d'yeux (`ry` du ellipse animé) — sauf en pose sleep
  - 🔥 Torches qui vacillent (fill color + opacity)
  - ✨ Sparkles pulsent en pose wave / proud
  - ☕ Vapeur de tasse en pose drink
  - 💤 Zzz qui apparaissent l'un après l'autre en pose sleep

### 🧠 Insights techniques

- **Confirmé : SMIL fonctionne dans un README GitHub** quand le SVG est chargé via `<img>` relatif au repo. Zéro latence, zéro Action supplémentaire.
- **Confirmé : impossible d'avoir "click sur mascotte → animation sur place"** — nécessite JS qui est strippé
- **Impossible d'avoir "click → scène change → reste sur profil sans refresh"** — nécessite JS/CSS custom. Trois options réelles : nav vers autre page (A), `<details>` (B), ou issue-based Action (C, avec latence)
- **Git rebase piège important** : pendant un rebase, `--ours`/`--theirs` sont INVERSÉS par rapport à un merge. Pour garder ses commits locaux pendant un `git rebase --continue`, utiliser `git checkout --theirs <file>`. Sinon on garde la version du remote (bot) et on écrase son propre travail — c'est arrivé une fois, on a dû refaire un commit correctif.

### 🚧 Ce que Ludwig fait entre les sessions

**Assets réels** : Ludwig reviendra quand il aura choisi et produit ses assets définitifs.

Options rappelées (voir `docs/ASSETS.md` pour détails complets) :
- Vroid Studio (gratuit, ~1 weekend)
- Commission Skeb/Fiverr (50-200€, 3-14 jours)
- Live2D
- Stable Diffusion + LoRA
- Packs itch.io

### 📅 Agenda quand Ludwig revient

1. **Intégrer les vrais assets** — remplacer les placeholders dans `assets/`
2. **Nommer** la guilde et l'hôtesse
3. **Enrichir l'arbre de dialogue** — plus de branches, plus de fins
4. **Compléter au moins 1 quête de plus** (SAO-Utils ou Estiam-RFID)
5. **(Optionnel) Brancher l'API Claude** pour dialogues auto-générés à partir des commits
