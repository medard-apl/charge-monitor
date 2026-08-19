import tkinter as tk
from tkinter import ttk, messagebox

from battery_monitor import BatteryMonitor
from notifier import Notifier


class ChargeMonitorApp:
    """
    Interface graphique principale de l'application.
    """

    def __init__(self, root):
        """
        Initialise l'application.
        """

        self.root = root

        # --------------------------------------------------
        # CONFIGURATION DE LA FENÊTRE
        # --------------------------------------------------

        self.root.title("Charge Monitor")
        self.root.geometry("500x420")
        self.root.resizable(False, False)

        # --------------------------------------------------
        # OBJETS MÉTIER
        # --------------------------------------------------

        self.battery_monitor = BatteryMonitor()
        self.notifier = Notifier()

        # --------------------------------------------------
        # VARIABLES DE L'APPLICATION
        # --------------------------------------------------

        # Le programme est-il actuellement actif ?
        self.running = False

        # Temps restant en secondes.
        self.remaining_seconds = 0

        # Dernier état détecté.
        self.current_state = None

        # Indique si la notification correspondant
        # au timeout a déjà été envoyée.
        self.timeout_notified = False

        # --------------------------------------------------
        # VARIABLES TKINTER
        # --------------------------------------------------

        self.duration_var = tk.StringVar(value="120")

        self.state_var = tk.StringVar(value="État : détection...")

        self.timer_var = tk.StringVar(value="02:00:00")

        self.status_var = tk.StringVar(value="Arrêté")

        self.battery_var = tk.StringVar(value="Batterie : -- %")

        # --------------------------------------------------
        # CRÉATION DE L'INTERFACE
        # --------------------------------------------------

        self.create_interface()

        # Détecter immédiatement l'état de la batterie.
        self.update_battery_state()

        # Lancer la boucle de surveillance.
        self.root.after(1000, self.update)

    # ======================================================
    # INTERFACE
    # ======================================================

    def create_interface(self):
        """
        Crée tous les éléments graphiques.
        """

        # Titre
        title = ttk.Label(
            self.root,
            text="🔋 Charge Monitor",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=(25, 10))

        # État de charge
        self.state_label = ttk.Label(
            self.root,
            textvariable=self.state_var,
            font=("Arial", 14)
        )

        self.state_label.pack(pady=10)

        # Pourcentage de la batterie
        self.battery_label = ttk.Label(
            self.root,
            textvariable=self.battery_var,
            font=("Arial", 12)
        )

        self.battery_label.pack(pady=5)

        # Compteur
        self.timer_label = ttk.Label(
            self.root,
            textvariable=self.timer_var,
            font=("Arial", 40, "bold")
        )

        self.timer_label.pack(pady=25)

        # --------------------------------------------------
        # PARAMÈTRE DE DURÉE
        # --------------------------------------------------

        duration_frame = ttk.Frame(self.root)

        duration_frame.pack(pady=10)

        ttk.Label(
            duration_frame,
            text="Durée du timeout (minutes) :"
        ).grid(row=0, column=0, padx=5)

        self.duration_entry = ttk.Entry(
            duration_frame,
            textvariable=self.duration_var,
            width=10
        )

        self.duration_entry.grid(row=0, column=1, padx=5)

        # --------------------------------------------------
        # BOUTONS
        # --------------------------------------------------

        button_frame = ttk.Frame(self.root)

        button_frame.pack(pady=20)

        self.start_button = ttk.Button(
            button_frame,
            text="▶ Démarrer",
            command=self.start
        )

        self.start_button.grid(
            row=0,
            column=0,
            padx=5
        )

        self.pause_button = ttk.Button(
            button_frame,
            text="⏸ Pause",
            command=self.pause,
            state="disabled"
        )

        self.pause_button.grid(
            row=0,
            column=1,
            padx=5
        )

        # --------------------------------------------------
        # STATUT
        # --------------------------------------------------

        ttk.Label(
            self.root,
            textvariable=self.status_var
        ).pack(pady=5)

    # ======================================================
    # DÉMARRAGE
    # ======================================================

    def start(self):
        """
        Démarre le compteur.
        """

        if self.running:
            return

        # Récupérer la durée saisie.
        try:
            duration_minutes = int(self.duration_var.get())

            if duration_minutes <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Durée invalide",
                "Veuillez entrer une durée entière supérieure à 0."
            )

            return

        # Conversion minutes -> secondes.
        self.remaining_seconds = duration_minutes * 60

        # Récupération de l'état actuel.
        state = self.battery_monitor.get_state()

        if state == "INCONNU":
            messagebox.showerror(
                "Erreur",
                "Impossible de détecter l'état de la batterie."
            )

            return

        self.current_state = state

        self.running = True
        self.timeout_notified = False

        self.status_var.set("Surveillance active")

        self.start_button.config(state="disabled")
        self.pause_button.config(state="normal")

        self.update_timer_display()

    # ======================================================
    # PAUSE
    # ======================================================

    def pause(self):
        """
        Met le compteur en pause.
        """

        self.running = False

        self.status_var.set("En pause")

        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")

    # ======================================================
    # DÉTECTION DE L'ÉTAT DE LA BATTERIE
    # ======================================================

    def update_battery_state(self):
        """
        Vérifie l'état actuel du PC et met à jour
        le pourcentage de batterie.
        """

        # Récupérer l'état de charge
        state = self.battery_monitor.get_state()

        # Récupérer le pourcentage de batterie
        percentage = self.battery_monitor.get_percentage()

        # --------------------------------------------------
        # AFFICHAGE DU POURCENTAGE
        # --------------------------------------------------

        if percentage is None:

            self.battery_var.set(
                "Batterie : inconnue"
            )

        else:

            self.battery_var.set(
                f"Batterie : {percentage:.0f} %"
            )

        # --------------------------------------------------
        # AFFICHAGE DE L'ÉTAT
        # --------------------------------------------------

        if state == "INCONNU":

            self.state_var.set(
                "État : impossible à déterminer"
            )

            return

        if state == "EN CHARGE":

            self.state_var.set(
                "⚡ État : EN CHARGE"
            )

        else:

            self.state_var.set(
                "🔋 État : PAS EN CHARGE"
            )

        # --------------------------------------------------
        # DÉTECTION D'UN CHANGEMENT D'ÉTAT
        # --------------------------------------------------

        if self.current_state is None:

            self.current_state = state

        elif state != self.current_state:

            self.handle_state_change(state)
            
    # ======================================================
    # CHANGEMENT D'ÉTAT
    # ======================================================

    def handle_state_change(self, new_state):
        """
        Gère le branchement ou le débranchement du chargeur.
        """

        old_state = self.current_state

        self.current_state = new_state

        # Si le programme est actif, un changement
        # de branchement/débranchement recommence
        # automatiquement un nouveau cycle.
        if self.running:

            # Récupération de la durée.
            try:
                duration_minutes = int(
                    self.duration_var.get()
                )

            except ValueError:
                return

            # Nouveau compteur.
            self.remaining_seconds = duration_minutes * 60

            # La notification du précédent cycle
            # n'est plus considérée comme envoyée.
            self.timeout_notified = False

            # Mise à jour du statut.
            if new_state == "EN CHARGE":

                self.status_var.set(
                    "Chargeur branché — nouveau cycle"
                )

            else:

                self.status_var.set(
                    "Chargeur débranché — nouveau cycle"
                )

    # ======================================================
    # BOUCLE PRINCIPALE
    # ======================================================

    def update(self):
        """
        Fonction exécutée toutes les secondes.

        Elle surveille :
        - l'état de la batterie ;
        - le compte à rebours ;
        - le timeout.
        """

        # Vérifier l'état de charge.
        self.update_battery_state()

        # Si le programme est actif :
        if self.running:

            # Si le compteur n'est pas terminé.
            if self.remaining_seconds > 0:

                self.remaining_seconds -= 1

                self.update_timer_display()

            else:

                # Le timeout vient d'être atteint.
                self.handle_timeout()

        # Reprogrammer cette fonction dans 1 seconde.
        self.root.after(1000, self.update)

    # ======================================================
    # TIMEOUT
    # ======================================================

    def handle_timeout(self):
        """
        Exécute l'action lorsque le compteur arrive à zéro.
        """

        # Éviter d'envoyer la notification chaque seconde.
        if self.timeout_notified:
            return

        self.timeout_notified = True

        # --------------------------------------------------
        # SI LE PC EST EN CHARGE
        # --------------------------------------------------

        if self.current_state == "EN CHARGE":

            self.notifier.notify_unplug()

            self.status_var.set(
                "⚠ Durée atteinte — débranchez le chargeur"
            )

        # --------------------------------------------------
        # SI LE PC N'EST PAS EN CHARGE
        # --------------------------------------------------

        elif self.current_state == "PAS EN CHARGE":

            self.notifier.notify_plug()

            self.status_var.set(
                "⚠ Durée atteinte — rebranchez le chargeur"
            )

    # ======================================================
    # AFFICHAGE DU TIMER
    # ======================================================

    def update_timer_display(self):
        """
        Convertit les secondes restantes en HH:MM:SS.
        """

        hours = self.remaining_seconds // 3600

        minutes = (
            self.remaining_seconds % 3600
        ) // 60

        seconds = self.remaining_seconds % 60

        self.timer_var.set(
            f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        )


# ==========================================================
# LANCEMENT DE L'APPLICATION
# ==========================================================

def main():
    """
    Point d'entrée de l'application.
    """

    root = tk.Tk()

    app = ChargeMonitorApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()