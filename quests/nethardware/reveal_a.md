# 🌡️ Diagnostic : *Pâte thermique dégradée*

## ✅ **BONNE RÉPONSE — La Guilde applaudit.**

*L'hôtesse hoche la tête, un sourire au coin des lèvres.*

> *« Bien vu, aventurier. La pâte thermique, avec le temps, sèche et perd sa
> capacité à transférer la chaleur. Résultat : le CPU chauffe pour rien,
> le ventilateur s'affole en compensation, et tout le système ralentit
> pour se protéger (**thermal throttling**). »*

---

## 🧭 Comment on l'a détecté

Les indices étaient tous là :

| Symptôme | Signification |
|---|---|
| CPU 92°C + Load 88% | Le CPU force pour tenir un workload modéré |
| Fan RPM 3200 | Le ventilateur tourne haut sans que ça baisse la température |
| GPU 74°C (normal) | Le problème est **isolé au CPU** → ce n'est pas l'ambient |
| Power Draw 180W | Consommation élevée pour un load pas énorme = inefficacité thermique |

Bref : **transfert thermique cassé côté CPU**, cause classique = pâte thermique HS.

---

## 🎁 Ce que fait le vrai projet

Cette quête est un cas type que mon projet **[nethardware-monitor](https://github.com/LeDeutsch/nethardware-monitor)** aurait détecté en temps réel :

- 📈 Surveillance continue de **CPU/GPU/RAM/Disk/Fan** avec seuils configurables
- 🚨 **Alerte automatique** quand la corrélation *"temp haute + fan haut + load modéré"* se déclenche
- 📊 Historique pour repérer la **dérive lente** (la pâte thermique ne meurt pas d'un coup — elle se dégrade sur des mois)
- 🌐 Web dashboard temps réel accessible depuis n'importe quel appareil du réseau

L'idée : **détecter le problème avant que la bête ne s'écroule.**

---

## 🏅 Tampon obtenu !

Ajoute *« Ingénieur des Constantes »* à ta carte d'aventurier.

- [→ Retour au tableau des quêtes](../README.md)
- [🏛️ Retour à la Guilde](../../README.md)
