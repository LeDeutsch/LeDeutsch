# 🗺️ ROADMAP

Ce qu'il reste à faire, classé par phase.

---

## ✅ MVP + Session 2 (livrés)

**Session 1 (MVP) :**
- [x] Structure de projet
- [x] Générateur de scène Python (composition en couches)
- [x] GitHub Action (cron 30min + on push)
- [x] Assets **placeholders** (fond, 6 poses mascotte, NPCs, props)
- [x] README profil
- [x] Hub de quêtes
- [x] 1 quête complète (nethardware) avec 4 reveals
- [x] 4 quêtes placeholder (sao-utils, estiam-rfid, unity-hierarchy, lulu)
- [x] Documentation (setup, assets, architecture, roadmap)

**Session 2 (dialog tree + scène vivante) :**
- [x] Refactor : 3 boutons de dialogue sous la scène (au lieu de scène cliquable)
- [x] Générateur produit 7 scènes (1 dynamique + 6 variantes par pose)
- [x] Arbre de dialogue basique (`dialog/greet.md`, `dialog/rest.md`, etc.)
- [x] Animations SMIL : respiration, clignements, torches vacillantes, sparkles, vapeur, Zzz

---

## 🎨 Phase 1 — Assets réels

Priorité : remplacer les placeholders par de vrais assets. Voir [ASSETS.md](ASSETS.md).

- [ ] Choisir la voie assets (Vroid recommandé pour MVP)
- [ ] **Fond de guilde** définitif (Midjourney ou commission)
- [ ] **Mascotte** en 6 poses cohérentes
- [ ] Nommer l'hôtesse (Skadi ? Iris ? Yuna ? à toi de voir)
- [ ] Nommer la guilde (« Guilde d'Aincrad » ? « Guilde des Bidouilleurs » ? etc.)
- [ ] NPCs de fond plus soignés (2-3 silhouettes)
- [ ] Props (papiers, tasses) plus jolis

**Coût estimé** : 0-150€ selon la voie choisie
**Effort** : 1 weekend (Vroid) à 2 semaines (commission)

---

## 📜 Phase 2 — Compléter les quêtes

Chaque quête placeholder à transformer en mini-jeu réel.

- [ ] **SAO-Utils** — « Traduis comme LeDeutsch » (3-5 rounds de traduction)
- [ ] **Estiam-RFID** — « Scan le bon badge » (4 badges, 1 valide)
- [ ] **Unity Hierarchy** — « Avant/Après » (2 images comparatives + explication)
- [ ] **LULU** — « Habille le composant » (3 choix CSS, 1 correct)
- [ ] **Quête cachée** débloquée à 5/5 → CV + contact

**Effort** : ~1h par quête pour rédiger, + assets d'illustration

---

## ✨ Phase 3 — Vitalité renforcée

- [x] ~~Micro-animations SMIL (breathing, blink, torch flicker)~~ ← fait en session 2
- [ ] **Répliques IA** : appel API Claude Haiku dans `pick_dialogue()`, la mascotte génère ses répliques en fonction du vrai commit message + son "personnage"
  - Ajouter `ANTHROPIC_API_KEY` dans les secrets du repo
  - Prompt système = fiche de perso de l'hôtesse (nom, personnalité, ton)
- [ ] **Poses supplémentaires** : `angry` (commit avec `revert`), `sleepy` (2h-6h), `surprised` (nouvelle release), `party` (dimanche)
- [ ] **Overlay saisonnier** : chapeau de Père Noël en décembre, citrouille Halloween, cœurs le 14 février
- [ ] **NPCs dynamiques** : plus il y a de commits récents = plus la guilde est peuplée
- [ ] **Snake des contribs** intégré en bas de README (via `Platane/snk`)
- [ ] **Enrichir l'arbre de dialogue** : plus de branches, achievements cachés

---

## 🎮 Phase 4 — Interactivité poussée

- [ ] **Système d'échecs jouable via issues** (bonus : chaque coup avance la scène — pion mangé = un NPC part)
- [ ] **Livre d'or** : les visiteurs signent via une issue, la mascotte les cite
- [ ] **Micro-anims SMIL** dans le SVG (blink, breathing) — attention : peut casser selon comment GitHub sert le SVG

---

## 🧪 Idées « pourquoi pas »

- Boss de fin invocable une fois toutes les quêtes complétées (Cthulhu-like ASCII)
- Compteur de visiteurs affiché comme "aventuriers accueillis aujourd'hui"
- Statistiques GitHub converties en fiche de perso RPG (STR = commits, INT = PRs, CHA = étoiles, LUCK = issues fermées)
- Playlist Spotify actuelle affichée sur le vinyle du fond
- Météo réelle de Paris → pluie sur la fenêtre de la guilde

---

## 📅 Priorité conseillée pour prochaine session

Karl reprendra quand il aura les vrais assets.

1. **Intégrer les vrais assets mascotte + fond** (Phase 1) — remplacer les placeholders
2. **Nommer** la guilde et l'hôtesse
3. **Enrichir l'arbre de dialogue** avec les vrais visuels
4. **Compléter 1 ou 2 quêtes** au format mini-jeu réel (SAO-Utils ou Estiam-RFID en priorité)
5. **Brancher l'API Claude pour les dialogues auto** (Phase 3) — mineur en effort, énorme en vivacité

Le reste vient au fil de l'eau.
