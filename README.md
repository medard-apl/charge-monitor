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
- ⏱️ Compte à rebours configurable, affiché sous forme d'anneau circulaire animé.
- 🔔 Notifications système.
- ▶️ Bouton pour démarrer la surveillance.
- ⏸️ Bouton pour mettre la surveillance en pause.
- 🔋 Affichage du niveau de batterie sous forme de barre colorée (vert / orange / rouge selon le niveau).
- ⚡ Badge d'état coloré (en charge / pas en charge / inconnu).
- 🔄 Redémarrage automatique du compteur lors d'un changement d'état.
- 🖥️ Interface graphique Tkinter avec thème sombre et rendu soigné.

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

## 🛠️ Technologies utilisées

Le projet utilise principalement :

- **Python 3**
- **Tkinter** — interface graphique
- **psutil** — récupération des informations relatives à la batterie
- **Plyer** — notifications système
- **PyInstaller** — génération de l'exécutable autonome (facultatif, pour le déploiement)

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
```

---

## ▶️ Lancer le projet en mode développement

"WINDOWS"
```
git clone https://github.com/medard-apl/charge-monitor.git

cd charge-monitor

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python main.py
```

"Linux / macOS"
```
git clone https://github.com/medard-apl/charge-monitor.git

cd charge-monitor

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python3 main.py
```

---

## 📦 Déployer l'application en mini app de bureau (sans terminal)

Pour ne plus jamais avoir à taper de commande, l'application peut être transformée en un **exécutable autonome** grâce à `PyInstaller`. Cette opération n'est à faire **qu'une seule fois** ; ensuite, il suffit de double-cliquer sur l'application comme n'importe quel logiciel installé.

### Étape unique (à faire une fois)

**Windows**
1. Double-cliquez sur `build.bat` (ou exécutez-le depuis l'explorateur de fichiers).
2. Patientez pendant l'installation des dépendances et la construction.
3. Une fois terminé, l'exécutable se trouve dans `dist\ChargeMonitor.exe`.

**Linux / macOS**
1. Rendez le script exécutable une première fois : `chmod +x build.sh`
2. Lancez-le : `./build.sh`
3. Une fois terminé, l'exécutable se trouve dans `dist/ChargeMonitor`.

### Utilisation au quotidien

- Créez un raccourci de `dist\ChargeMonitor.exe` (clic droit → *Envoyer vers → Bureau*) pour l'avoir directement sur votre Bureau ou dans votre menu Démarrer.
- Vous pouvez ensuite lancer Charge Monitor en double-cliquant simplement dessus, sans jamais ouvrir de terminal.
- Le script `build.bat` / `build.sh` n'a besoin d'être relancé que si vous modifiez le code source de l'application.

> 💡 Astuce : pour un rendu encore plus « app native », vous pouvez ajouter un fichier `icon.ico` (Windows) ou `icon.icns` (macOS) à la racine du projet, puis ajouter l'option `--icon=icon.ico` à la commande PyInstaller dans `build.bat`.