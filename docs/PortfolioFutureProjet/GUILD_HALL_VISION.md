# 🏰 LeDeutsch's Guild Hall — Vision & MVP

*Document de référence — à relire quand tu voudras te lancer.*

---

## 1. Le concept en une phrase

Le profil GitHub de Ludwig (LeDeutsch) est mis en scène comme une **guilde d'aventuriers JRPG**. Ce document couvre l'extension du projet : transformer le README vivant en point d'entrée vers un **portfolio narratif** et une **application web gamifiée** où les visiteurs deviennent des aventuriers, apprennent à coder, et peuvent aider sur de vrais projets — le tout gratuitement.

---

## 2. Ce qui existe déjà (base solide)

Le README `LeDeutsch/LeDeutsch` fonctionne et contient :

- Une scène SVG générée par un script Python (`scripts/generate_scene.py`), composée en couches (fond, NPCs, props, lumière, mascotte, dialogue)
- Une **GitHub Action** qui régénère la scène toutes les 30 min et à chaque push (heure du jour, activité récente, workload → pose et lumière changent)
- 6 poses de mascotte hôtesse (encore en placeholders — commission d'artiste déjà lancée pour les remplacer)
- Un arbre de dialogue basique (3 boutons : Saluer / Quêtes / Repos)
- Des animations SMIL (respiration, clignements, torches, sparkles, vapeur, Zzz)
- Un hub de quêtes façon README (1 quête complète : nethardware-monitor ; 4 placeholders : SAO-Utils, Estiam-RFID, Unity Hierarchy, LULU)

C'est la fondation. Tout ce qui suit s'y branche.

---

## 3. L'extension : le Maître de Guilde

**L'idée centrale** : Ludwig apparaît dans le README comme le **Maître de Guilde** (par événement, pas en permanence). Un bouton "Contacter le Maître de Guilde" ouvre un **portfolio** qui fonctionne en deux modes :

- **Mode visiteur** (sans compte) : vitrine JRPG des faits d'armes du Maître de Guilde — *"Dinspel Ludwig, Rang A"* — avec une propagande sympathique : *"Vous aussi, devenez un aventurier !"*
- **Mode connecté** (via GitHub OAuth) : le visiteur crée un compte, obtient une **fiche de personnage** générée à partir de ses vraies stats GitHub, et accède à un **tableau de quêtes**.

### Les 3 objectifs du projet

1. **Fournir et maintenir à jour un portfolio** — vitrine de projets et d'exploits, régénérée automatiquement
2. **Cohérence visuelle avec le README** — même univers, mêmes assets, même ton narratif
3. **Inciter (sans forcer) à contribuer / committer** — via la gamification : XP, rangs, badges, classement. Le ressort est le même que Duolingo ou les achievements Steam : transformer "je devrais contribuer" en "je veux monter en rang"

---

## 4. Architecture technique — 100% gratuite

### Le blocage GitHub Pages, expliqué

GitHub Pages ne sert que du statique : pas de code serveur, pas de secrets, pas de réception de webhooks. Impossible d'y faire l'échange OAuth GitHub tout seul (il faut un `client_secret` gardé côté serveur). **Solution : déléguer l'auth à Supabase**, qui garde le secret et fait l'échange à la place du site.

### Répartition retenue

| Composant | Hébergement | Rôle | Coût |
|---|---|---|---|
| README profil | GitHub (existant) | Scène vivante + event Maître de Guilde + lien vers le portfolio | Gratuit |
| Portfolio visiteur | **GitHub Pages** | Site statique, vitrine JRPG des exploits, CTA "devenir aventurier". Régénéré par une Action (même pattern que le générateur de scène actuel) | Gratuit |
| App aventurier | **Vercel** + **Supabase** | Auth GitHub OAuth, fiche de perso, tableau de quêtes, XP/rangs/badges | Gratuit (plan Hobby / free tier, très large marge) |
| Nom de domaine perso | Optionnel | `tonnom.dev` au lieu de `tonnom.vercel.app` | ~10-15 €/an *(seul coût possible, non nécessaire)* |

Le lien entre le portfolio (GitHub Pages) et l'app (Vercel) est un simple bouton "Devenir aventurier" — pas de session partagée nécessaire, juste une redirection.

### Ce qui reste réellement limité

Seule la validation **automatique** d'une quête au merge d'une PR nécessite un webhook (réception de requête serveur) — impossible sur GitHub Pages. Solution légère : une Supabase Edge Function (gratuite) dédiée à ça. Pour le MVP, une validation **manuelle** suffit largement.

---

## 5. Les deux types de quêtes

Un point clé pour que le jeu ait du contenu même à 0 joueur :

| Type | Description | Dépend d'autres joueurs ? |
|---|---|---|
| **Quêtes vivantes** | Vraie demande de PR sur un vrai repo (le tien, puis ceux d'autres aventuriers une fois le marketplace ouvert) | Oui, en partie (mais jouable en solo sur tes propres repos) |
| **Quêtes narratives** | Mini-jeux que Ludwig conçoit lui-même pour enseigner un concept (QCM de code, fill-in-the-blank, repère-le-bug, avant/après, glisser-déposer) — extension directe des quêtes déjà esquissées (SAO-Utils, Estiam-RFID, Unity Hierarchy, LULU) | Non — jouable seul, aucune dépendance |

Les deux alimentent la **même fiche de personnage** (XP, rang, badges communs).

> **Note technique** : éviter l'exécution de code arbitraire côté serveur pour le MVP (sécurité + complexité). QCM / fill-in-the-blank / repère-le-bug couvrent large sans ce risque. Exécution de vrai code = amélioration V2 (API gratuites existantes comme Piston).

---

## 6. Stats GitHub → stats RPG

Formule de départ (à ajuster) :

- **STR** = nombre de commits
- **INT** = PRs mergées
- **CHA** = stars reçues
- **LUCK** = issues fermées
- **Niveau / Rang** (F → S) = combinaison pondérée des stats ci-dessus

Recalcul à la connexion ou via bouton "rafraîchir" — pas de polling temps réel (évite de cramer le rate limit API GitHub).

---

## 7. Modèle de données (esquisse)

Tables Supabase à prévoir :

- `users` — profil, GitHub id, stats calculées, XP, rang
- `quests` — titre, description, type (`live` / `narrative`), repo cible (si `live`), difficulté, tags, récompense XP
- `completions` — lien user ↔ quest, statut, date, lien PR (si applicable)
- `badges` — catalogue de badges + table de liaison user ↔ badges débloqués

Le marketplace ouvert (n'importe qui poste une quête) est juste un changement de permission sur `quests` — pas de refonte nécessaire.

---

## 8. Roadmap suggérée

### MVP réduit (le plus rapide à livrer, dans l'ordre)

1. **Event "Maître de Guilde"** dans le README existant + bouton vers le portfolio (même si le portfolio est encore minimal)
2. **Portfolio visiteur statique** sur GitHub Pages (bio façon fiche de perso, projets, CTA "devenir aventurier")
3. **App minimale** sur Vercel + Supabase : connexion GitHub OAuth + fiche de perso auto-générée
4. **1 à 2 quêtes narratives jouables en solo** (transformer SAO-Utils ou Estiam-RFID en vrai mini-jeu)
5. Validation manuelle des quêtes, marketplace fermé (Ludwig seul poste des quêtes)

### Post-MVP (Phase 2, quand il y a de la traction)

- Ouverture du marketplace (n'importe quel aventurier poste une quête sur son repo)
- Automatisation de la validation via webhook GitHub → Supabase Edge Function
- Classement public des aventuriers
- Répliques IA de la mascotte (API Claude, déjà prévu dans la roadmap du README)
- Overlays saisonniers, NPCs dynamiques, poses supplémentaires (déjà dans la roadmap existante)

---

## 9. Coûts — récapitulatif

**Tout est gratuit**, sauf un nom de domaine personnalisé optionnel (~10-15 €/an, non nécessaire au lancement). Aucune publicité, aucun abonnement, aucun compte payant côté joueurs.

---

## 10. Pourquoi ce projet vaut le coup

Au-delà du fun, le projet devient lui-même une pièce de portfolio : concevoir un système d'auth OAuth, une architecture multi-hébergement gratuite, de la génération procédurale SVG et un moteur de gamification est un vrai projet technique complet à présenter — pas seulement une décoration de profil.

---

*Document généré le 27 juillet 2026 à partir d'une session de brainstorm. À relire et adapter au moment de se lancer.*
