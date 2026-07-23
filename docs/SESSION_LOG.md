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
2. **Nommer** la guilde et l'hôtesse (à faire par Karl entre les sessions, cool)
3. **Compléter 1 ou 2 quêtes** au format mini-jeu vraiment jouable
4. **Optionnel** — brancher l'API Claude (Haiku, très pas cher) pour que la mascotte génère ses dialogues à partir du vrai commit message + un system prompt "persona"

### 🧩 Points techniques à retenir pour la reprise

- Le repo profil est `LeDeutsch/LeDeutsch` sur GitHub, cloné en local dans `c:/Users/lespe/OneDrive/Bureau/LeDeutsch-profile/`
- Le workflow tourne toutes les 30 min (cron) ET à chaque push
- Le token GitHub qu'on a utilisé pour le push a les scopes `repo` + `workflow`
- Le nethardware-monitor de Karl est un projet **totalement séparé** — les deux n'ont aucun lien de code, juste un lien narratif (nethardware-monitor est présenté comme une quête dans le profil)
- Karl (l'user) est étudiant à ESTIAM, à Paris, avatar anime (Ichigo de Bleach), aime l'esthétique JRPG/anime type Miku wallpaper

### 📂 Fichiers clés à ouvrir en début de reprise

- Ce fichier
- `docs/ROADMAP.md` — pour voir les phases planifiées
- `docs/ASSETS.md` — pour la voie assets choisie
- `scripts/generate_scene.py` — la logique centrale, à étendre pour toute nouvelle règle
- `assets/` — les placeholders à remplacer

---

## 🗓️ Session 2 — [à venir]

*Écrire ici les décisions et avancées de la prochaine session.*
