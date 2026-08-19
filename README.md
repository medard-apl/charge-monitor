# 🔋 Charge Monitor

Application Python légère permettant de surveiller le temps passé par un ordinateur en charge ou hors charge.

L'application détecte automatiquement l'état de la batterie et lance un compte à rebours lorsque la surveillance est activée.

Lorsque le délai configuré est atteint :

- ⚡ Si le PC est en charge : une notification indique à l'utilisateur qu'il peut débrancher son chargeur.
- 🔋 Si le PC n'est pas en charge : une notification indique à l'utilisateur qu'il peut rebrancher son chargeur.

Le programme recommence ensuite un nouveau cycle lorsqu'un changement d'état de charge est détecté.

---

## 📸 Fonctionnalités

### Fonctionnalités principales

- 🔌 Détection automatique du branchement/débranchement du chargeur.
- ⏱️ Compte à rebours configurable.
- 🔔 Notifications système.
- ▶️ Bouton pour démarrer la surveillance.
- ⏸️ Bouton pour mettre la surveillance en pause.
- 🔋 Affichage du niveau actuel de batterie.
- ⚡ Affichage de l'état actuel de charge.
- 🔄 Redémarrage automatique du compteur lors d'un changement d'état.
- 🖥️ Interface graphique avec Tkinter.

### Configuration du timeout 

L'utilisateur peut définir la durée du compteur directement depuis l'interface.

Exemples :

| Durée | Timeout |
|---|---:|
| 30 | 30 minutes |
| 60 | 1 heure |
| 120 | 2 heures |
| 180 | 3 heures |

La durée est exprimée en minutes.

---

# 🛠️ Technologies utilisées

Le projet utilise principalement :

- **Python 3**
- **Tkinter** — interface graphique
- **psutil** — récupération des informations relatives à la batterie
- **Plyer** — notifications système

## Bibliothèques

### Tkinter

Tkinter est utilisé pour construire l'interface graphique.

Il est généralement inclus avec les installations standards de Python.

### psutil

`psutil` permet notamment de récupérer :

- le niveau de batterie ;
- l'état de branchement du chargeur.

Exemple :

```python
battery = psutil.sensors_battery()

battery.percent
battery.power_plugged

###  Installation du projet

"WINDOWS"
git clone https://github.com/medard-apl/charge-monitor.git
cd charge-monitor
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py

"Linux / macOS"
git clone https://github.com/medard-apl/charge-monitor.git
cd charge-monitor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py