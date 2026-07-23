# 🛠️ SETUP — Installation & Publication

Guide pas-à-pas pour passer de ce dossier local au profil GitHub vivant.

---

## 1) Créer le repo GitHub "profil"

GitHub reconnaît un repo **spécial** dont le nom est identique à ton pseudo. Son README s'affiche sur ta page de profil.

1. Va sur https://github.com/new
2. **Repository name** : `LeDeutsch` (exactement identique à ton pseudo, casse comprise)
3. **Public** ✅
4. **Add a README file** : ❌ (on a déjà le nôtre)
5. **Add .gitignore** : ❌ (on a déjà le nôtre)
6. Clique **Create repository**

GitHub te dira *"LeDeutsch/LeDeutsch is a ✨ special ✨ repository"* — c'est bon signe.

---

## 2) Pousser ce dossier vers le repo

Depuis ce dossier (`LeDeutsch-profile/`), dans PowerShell :

```powershell
git init
git branch -M main
git add .
git commit -m "feat: initial guild hall setup"
git remote add origin https://github.com/LeDeutsch/LeDeutsch.git
git push -u origin main
```

Va sur `https://github.com/LeDeutsch` — tu devrais voir la scène apparaître (en placeholder).

---

## 3) Autoriser l'Action à commit

L'Action a besoin de pousser les mises à jour de la scène. Par défaut GitHub bloque.

1. Va sur https://github.com/LeDeutsch/LeDeutsch/settings/actions
2. Section **Workflow permissions** → coche **Read and write permissions**
3. **Save**

---

## 4) Déclencher la première génération

Deux options :

- **Attendre** : le cron tourne toutes les 30 min, la scène se mettra à jour toute seule.
- **Forcer** : va sur l'onglet *Actions*, clique sur `Update Guild Scene`, puis **Run workflow** → `main` → Run.

Au bout de ~30 secondes, `output/scene.svg` sera régénéré avec ton contexte actuel (heure serveur, ton dernier commit).

---

## 5) Vérifier localement (optionnel)

Pour tester la génération sur ta machine avant de push :

```powershell
cd LeDeutsch-profile
python scripts/generate_scene.py
```

Ouvre `output/scene.svg` dans un navigateur pour voir la scène. Modifie l'heure de ton système ou attends que l'Action se déclenche pour voir la lumière changer.

---

## 6) Personnaliser (nom de guilde, hôtesse, projets)

Voir [ROADMAP.md](ROADMAP.md) pour la liste des choses à personnaliser après la mise en ligne.

Voir [ASSETS.md](ASSETS.md) pour remplacer les placeholders SVG par de vrais assets (Vroid, IA, commission).

---

## ⚠️ Troubleshooting

**L'Action échoue avec "Permission denied"** → étape 3 pas faite.

**La scène ne se met pas à jour** → vérifie que le workflow a bien tourné (onglet Actions). Cache GitHub peut mettre 1-2 min à s'invalider.

**L'image ne s'affiche pas sur le profil** → le repo doit être **public** ET porter EXACTEMENT ton pseudo (respect de la casse : `LeDeutsch` ≠ `ledeutsch`).
