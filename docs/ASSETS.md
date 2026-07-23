# 🎨 ASSETS — Remplacer les placeholders

Les SVG actuels dans `assets/` sont des **placeholders** — moches mais fonctionnels. Ce document liste toutes les options pour obtenir de vrais assets, avec coût, effort, et cohérence.

---

## 🎯 Ce qu'il faut produire

| Asset | Format | Dimensions cibles (dans le viewBox 1200×600) |
|---|---|---|
| **Fond de guilde** | 1 SVG ou 1 PNG converti en SVG | 1200×600 pleine scène |
| **Mascotte hôtesse** | 6 SVG (1 par pose) | ~200×250 centrée à x=650 y=280 |
| **NPCs de fond** | 1 SVG regroupant 3-4 silhouettes | intégré dans le layer |
| **Props dynamiques** | 1 SVG par prop (papers, coffee, etc.) | posés sur le comptoir |

Les 6 poses de mascotte à produire : `idle`, `wave`, `sleep`, `code`, `drink`, `proud`.

---

## 🏆 Option A — Vroid Studio (GRATUIT, ma reco pour MVP)

**Qu'est-ce que c'est :** logiciel japonais gratuit (Pixiv) qui permet de créer un personnage anime 3D personnalisable et de le rendre en 2D.

**Site :** https://vroid.com/en/studio

**Workflow :**
1. Télécharge Vroid Studio (Windows, gratuit)
2. Suis un tuto YouTube "Vroid Studio tutorial 2024" (~30 min)
3. Modélise ta perso : cheveux, visage, tenue de guilde (vest + apron)
4. Pour chaque pose : **pose la perso**, cadre-la de face waist-up, **screenshot fond transparent**
5. Convertis chaque PNG en SVG (via https://convertio.co/png-svg/ ou Inkscape)
6. Remplace les fichiers dans `assets/mascot/`

**✅ Avantages**
- Cohérence 100% garantie entre poses (même perso, même vêtements)
- Style anime cel-shaded très populaire (Genshin, BanG Dream)
- Extensible à volonté (nouvelle pose = 5 min)
- Utilisable commercialement

**❌ Inconvénients**
- ~2-3h d'apprentissage initial
- Rendu 3D → PNG → SVG perd un peu de fluidité
- Personnage a un "look Vroid" reconnaissable

**Coût :** 0€

---

## 🎨 Option B — Live2D (payant mais réutilisable)

**Qu'est-ce que c'est :** logiciel qui anime UN dessin en découpant les parties (yeux, bouche, cheveux, bras). Une seule illustration → infinité de micro-anims.

**Site :** https://www.live2d.com/en/cubism/

**Workflow :**
1. Faire dessiner ta mascotte par un·e artiste (~50-150€ sur Skeb/Fiverr) OU la dessiner toi-même
2. Découper les parties dans Photoshop/Krita
3. Rigger dans Live2D Cubism (Free edition suffit)
4. Exporter des poses statiques en PNG puis SVG

**✅ Avantages**
- Plus vivant qu'un sprite (micro-anims impossibles sinon)
- Style illustration 2D, moins "3D generic" que Vroid
- Une seule asset source → toutes les poses en dérivent

**❌ Inconvénients**
- Nécessite l'illustration initiale (coût ou temps)
- Courbe d'apprentissage Live2D plus rude que Vroid
- Cubism Pro : 105 USD/an (Free suffit pour l'usage README)

**Coût :** 0€ (soft) + 0-150€ (illustration)

---

## 🤖 Option C — IA générative (Stable Diffusion, Midjourney, NovelAI)

**Qu'est-ce que c'est :** génération d'images à partir de prompts textuels.

**Le vrai problème :** la **cohérence** entre plusieurs poses est très difficile.

### C.1 — Midjourney / NovelAI (facile mais cohérence limitée)

**Sites :** https://midjourney.com | https://novelai.net

**Workflow :**
1. Génère le **fond** avec un prompt type :
   > *"anime JRPG guild hall interior, warm cozy lighting, reception counters, fantasy tavern atmosphere, wide angle isometric view, detailed background art, no characters"*
2. Génère la mascotte avec un prompt fixe et le paramètre `--seed` bloqué pour maximiser la cohérence entre poses :
   > *"anime girl guild receptionist, brown long hair, red vest, white blouse, gold ribbon, front view, waist up, [POSE], white background"*
3. Retouche dans un éditeur pour les incohérences (couleur cheveux qui varie, etc.)

**✅ Avantages**
- Rapide (30 min pour tout)
- Style anime très propre
- Fond one-shot excellent

**❌ Inconvénients**
- Cohérence character-sheet imparfaite (les vêtements changent subtilement)
- Coût abo : ~10-30€/mois
- Licence : vérifier les CGU pour usage commercial

**Coût :** ~10-30€ (1 mois d'abo)

### C.2 — Stable Diffusion + LoRA (technique mais gratuit)

**Site :** local via https://github.com/AUTOMATIC1111/stable-diffusion-webui

**Workflow :**
1. Génère 20+ images de ta perso avec variations
2. Entraîne une **LoRA** dessus (~30 min sur GPU)
3. Utilise cette LoRA pour générer les 6 poses → cohérence quasi-parfaite

**✅ Avantages**
- Gratuit après le setup
- Cohérence excellente
- Contrôle total

**❌ Inconvénients**
- Setup technique (nécessite GPU 8GB+ ou Colab)
- ~1 après-midi d'apprentissage

**Coût :** 0€ (si tu as le hardware) ou ~5€ Colab

---

## 💰 Option D — Commission d'artiste (le meilleur rendu)

**Où trouver :**
- **Skeb** (https://skeb.jp) — Japonais, spécialisé illustration anime, ~50-200€ par pack. Excellent style.
- **Fiverr** (https://fiverr.com) — international, filtre "anime character sheet", ~50-300€. Qualité très variable, lis les avis.
- **VGen** (https://vgen.co) — plateforme dédiée aux artistes VTuber/game, ~80-400€
- **ArtStation** (https://artstation.com) — pros, ~200-800€

**Workflow :**
1. Rédige un **character brief** : nom, âge, personnalité, style vestimentaire, univers (guilde d'aventuriers), 6 poses attendues
2. Fournis 2-3 images de référence (style et outfit)
3. Commande un **character sheet** avec les 6 poses front-view waist-up
4. Livraison PNG haute résolution → convertis en SVG (Inkscape trace bitmap ou convertio.co)

**✅ Avantages**
- Qualité artistique maximale
- Style 100% original, unique à ton profil
- Utilisation commerciale négociée dans le contrat
- Tu peux commander de nouvelles poses plus tard chez la·le même artiste (cohérence garantie)

**❌ Inconvénients**
- Coût : 50-400€
- Délai : 3-14 jours
- Chercher un·e artiste dont le style te plaît prend du temps

**Coût :** 50-400€

---

## 🖼️ Option E — Packs d'assets existants (rapide, générique)

**Sites :**
- **itch.io** (https://itch.io/game-assets/tag-character-sprites) — énorme catalogue, gratuit à 20€
- **OpenGameArt** (https://opengameart.org) — 100% gratuit, licences claires
- **Kenney.nl** (https://kenney.nl) — gratuit, style clean, top pour les props
- **Craftpix** (https://craftpix.net) — payant, très haute qualité anime/pixel art

**Workflow :**
1. Cherche `"anime girl sprite pack"` ou `"visual novel character"` ou `"pixel art receptionist"`
2. Vérifie la licence (CC0 = libre total, CC-BY = crédit obligatoire)
3. Récupère les 6 poses depuis le pack
4. Adapte si besoin (colorimétrie, taille)

**✅ Avantages**
- Instantané
- Cohérence parfaite (même pack)
- Gratuit à peu cher

**❌ Inconvénients**
- Style pas 100% "toi"
- D'autres profils peuvent utiliser le même pack

**Coût :** 0-20€

---

## 🎨 Option F — Fond de scène : ma reco spécifique

Le **fond** est un cas facile : il est **fixe**, pas besoin de cohérence entre plusieurs versions.

Meilleure approche : **une seule illustration IA** (Midjourney ou NovelAI, 5 min de génération), puis conversion en SVG.

Prompt suggéré :
```
anime JRPG guild hall interior, cozy fantasy tavern reception,
warm torchlight, wooden counters in U-shape, quest board on wall,
window with sky, no characters, wide angle painting, Studio Ghibli style
--ar 2:1 --stylize 300
```

Ensuite dans Inkscape : `Path > Trace Bitmap > Colors` pour convertir en SVG vectoriel, ou garde en PNG et charge-le via `<image href="..."/>` dans le SVG parent.

---

## 📋 Récapitulatif décisionnel

| Ton profil = | Reco |
|---|---|
| Je veux tester vite et pas cher | **Option A (Vroid) + Fond IA** |
| Je veux un rendu pro sans effort | **Option D (commission Skeb)** |
| Je veux un style original que je maîtrise | **Option D + Live2D pour animer** |
| Je suis technique et j'aime bricoler | **Option C.2 (LoRA)** |
| Je veux juste que ça marche, style importe peu | **Option E (pack itch.io)** |

Mon avis final : **Option A (Vroid) pour la mascotte + Option F (IA one-shot) pour le fond**. Coût 0-15€, résultat très correct, tu contrôles tout, et si un jour tu veux upgrade tu remplaces juste les fichiers dans `assets/`.
