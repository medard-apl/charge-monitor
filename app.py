import tkinter as tk
from tkinter import ttk, messagebox

from battery_monitor import BatteryMonitor
from notifier import Notifier


# ==========================================================
# PALETTE DE COULEURS
# ==========================================================

COLORS = {
    "bg": "#1a1b26",
    "card": "#20222f",
    "border": "#2f3549",
    "text_primary": "#c0caf5",
    "text_secondary": "#7982a9",
    "accent_blue": "#7aa2f7",
    "accent_blue_dark": "#5a7fd6",
    "accent_green": "#9ece6a",
    "accent_orange": "#e0af68",
    "accent_red": "#f7768e",
}


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
        self.root.geometry("480x620")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg"])

        self.setup_styles()

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

        # Durée totale du cycle en cours (pour le minuteur circulaire).
        self.total_seconds = 0

        # Dernier état détecté.
        self.current_state = None

        # Indique si la notification correspondant
        # au timeout a déjà été envoyée.
        self.timeout_notified = False

        # --------------------------------------------------
        # VARIABLES TKINTER
        # --------------------------------------------------

        self.duration_var = tk.StringVar(value="120")

        self.state_var = tk.StringVar(value="Détection...")

        self.timer_var = tk.StringVar(value="02:00:00")

        self.status_var = tk.StringVar(value="Arrêté")

        self.battery_var = tk.StringVar(value="-- %")

        # --------------------------------------------------
        # CRÉATION DE L'INTERFACE
        # --------------------------------------------------

        self.create_interface()

        # Détecter immédiatement l'état de la batterie.
        self.update_battery_state()

        # Lancer la boucle de surveillance.
        self.root.after(1000, self.update)

    # ======================================================
    # STYLES
    # ======================================================

    def setup_styles(self):
        """
        Configure les styles ttk pour coller au thème sombre.
        """

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Accent.TButton",
            background=COLORS["accent_blue"],
            foreground="#12131c",
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
            focusthickness=0,
            padding=(18, 10),
        )
        style.map(
            "Accent.TButton",
            background=[
                ("active", COLORS["accent_blue_dark"]),
                ("disabled", COLORS["border"]),
            ],
            foreground=[("disabled", COLORS["text_secondary"])],
        )

        style.configure(
            "Ghost.TButton",
            background=COLORS["card"],
            foreground=COLORS["text_primary"],
            font=("Segoe UI", 11, "bold"),
            borderwidth=1,
            focusthickness=0,
            padding=(18, 10),
        )
        style.map(
            "Ghost.TButton",
            background=[
                ("active", COLORS["border"]),
                ("disabled", COLORS["card"]),
            ],
            foreground=[("disabled", COLORS["text_secondary"])],
        )

        style.configure(
            "Dark.TEntry",
            fieldbackground=COLORS["card"],
            foreground=COLORS["text_primary"],
            insertcolor=COLORS["text_primary"],
            borderwidth=1,
            padding=8,
        )

    # ======================================================
    # INTERFACE
    # ======================================================

    def create_interface(self):
        """
        Crée tous les éléments graphiques.
        """

        # --------------------------------------------------
        # TITRE
        # --------------------------------------------------

        header = tk.Frame(self.root, bg=COLORS["bg"])
        header.pack(pady=(28, 6))

        tk.Label(
            header,
            text="🔋 Charge Monitor",
            font=("Segoe UI", 22, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["text_primary"],
        ).pack()

        tk.Label(
            header,
            text="Surveillance intelligente de la charge",
            font=("Segoe UI", 10),
            bg=COLORS["bg"],
            fg=COLORS["text_secondary"],
        ).pack(pady=(2, 0))

        # --------------------------------------------------
        # BADGE D'ÉTAT
        # --------------------------------------------------

        badge = tk.Frame(self.root, bg=COLORS["card"], highlightbackground=COLORS["border"], highlightthickness=1)
        badge.pack(pady=16, ipadx=14, ipady=8)

        self.state_dot = tk.Canvas(badge, width=14, height=14, bg=COLORS["card"], highlightthickness=0)
        self.state_dot_id = self.state_dot.create_oval(2, 2, 12, 12, fill=COLORS["text_secondary"], outline="")
        self.state_dot.grid(row=0, column=0, padx=(10, 8))

        tk.Label(
            badge,
            textvariable=self.state_var,
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["card"],
            fg=COLORS["text_primary"],
        ).grid(row=0, column=1, padx=(0, 10))

        # --------------------------------------------------
        # MINUTEUR CIRCULAIRE
        # --------------------------------------------------

        ring_frame = tk.Frame(self.root, bg=COLORS["bg"])
        ring_frame.pack(pady=(4, 10))

        self.ring_size = 220
        self.ring_canvas = tk.Canvas(
            ring_frame,
            width=self.ring_size,
            height=self.ring_size,
            bg=COLORS["bg"],
            highlightthickness=0,
        )
        self.ring_canvas.pack()

        pad = 14
        self.ring_bbox = (pad, pad, self.ring_size - pad, self.ring_size - pad)

        self.ring_canvas.create_oval(
            *self.ring_bbox,
            outline=COLORS["border"],
            width=14,
        )

        self.ring_arc_id = self.ring_canvas.create_arc(
            *self.ring_bbox,
            start=90,
            extent=-360,
            style=tk.ARC,
            outline=COLORS["accent_blue"],
            width=14,
        )

        center = self.ring_size / 2

        self.ring_text_id = self.ring_canvas.create_text(
            center,
            center - 8,
            text=self.timer_var.get(),
            fill=COLORS["text_primary"],
            font=("Segoe UI", 24, "bold"),
        )

        self.ring_subtext_id = self.ring_canvas.create_text(
            center,
            center + 22,
            text="restant",
            fill=COLORS["text_secondary"],
            font=("Segoe UI", 10),
        )

        # --------------------------------------------------
        # NIVEAU DE BATTERIE
        # --------------------------------------------------

        battery_frame = tk.Frame(self.root, bg=COLORS["bg"])
        battery_frame.pack(pady=(6, 14), fill="x", padx=60)

        row = tk.Frame(battery_frame, bg=COLORS["bg"])
        row.pack(fill="x")

        tk.Label(
            row,
            text="Batterie",
            font=("Segoe UI", 10),
            bg=COLORS["bg"],
            fg=COLORS["text_secondary"],
        ).pack(side="left")

        tk.Label(
            row,
            textvariable=self.battery_var,
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["text_primary"],
        ).pack(side="right")

        self.battery_bar_width = 340
        self.battery_bar = tk.Canvas(
            battery_frame,
            width=self.battery_bar_width,
            height=10,
            bg=COLORS["bg"],
            highlightthickness=0,
        )
        self.battery_bar.pack(pady=(6, 0))

        self.battery_bar.create_rectangle(
            0, 0, self.battery_bar_width, 10,
            fill=COLORS["card"], outline="",
        )
        self.battery_bar_fill = self.battery_bar.create_rectangle(
            0, 0, 0, 10,
            fill=COLORS["accent_green"], outline="",
        )

        # --------------------------------------------------
        # PARAMÈTRE DE DURÉE
        # --------------------------------------------------

        duration_frame = tk.Frame(self.root, bg=COLORS["bg"])
        duration_frame.pack(pady=10)

        tk.Label(
            duration_frame,
            text="Durée du timeout (minutes)",
            font=("Segoe UI", 10),
            bg=COLORS["bg"],
            fg=COLORS["text_secondary"],
        ).grid(row=0, column=0, padx=(0, 10))

        self.duration_entry = ttk.Entry(
            duration_frame,
            textvariable=self.duration_var,
            width=8,
            style="Dark.TEntry",
            justify="center",
        )
        self.duration_entry.grid(row=0, column=1)

        # --------------------------------------------------
        # BOUTONS
        # --------------------------------------------------

        button_frame = tk.Frame(self.root, bg=COLORS["bg"])
        button_frame.pack(pady=20)

        self.start_button = ttk.Button(
            button_frame,
            text="▶  Démarrer",
            command=self.start,
            style="Accent.TButton",
        )
        self.start_button.grid(row=0, column=0, padx=6)

        self.pause_button = ttk.Button(
            button_frame,
            text="⏸  Pause",
            command=self.pause,
            style="Ghost.TButton",
            state="disabled",
        )
        self.pause_button.grid(row=0, column=1, padx=6)

        # --------------------------------------------------
        # STATUT
        # --------------------------------------------------

        tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            bg=COLORS["bg"],
            fg=COLORS["text_secondary"],
        ).pack(pady=(4, 10))

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
        self.total_seconds = self.remaining_seconds

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

            self.battery_var.set("inconnue")
            self.battery_bar.coords(self.battery_bar_fill, 0, 0, 0, 10)

        else:

            self.battery_var.set(f"{percentage:.0f} %")

            if percentage >= 50:
                bar_color = COLORS["accent_green"]
            elif percentage >= 20:
                bar_color = COLORS["accent_orange"]
            else:
                bar_color = COLORS["accent_red"]

            fill_width = self.battery_bar_width * (percentage / 100)

            self.battery_bar.coords(
                self.battery_bar_fill, 0, 0, fill_width, 10
            )
            self.battery_bar.itemconfig(
                self.battery_bar_fill, fill=bar_color
            )

        # --------------------------------------------------
        # AFFICHAGE DE L'ÉTAT
        # --------------------------------------------------

        if state == "INCONNU":

            self.state_var.set("Impossible à déterminer")
            self.state_dot.itemconfig(self.state_dot_id, fill=COLORS["text_secondary"])

            return

        if state == "EN CHARGE":

            self.state_var.set("⚡ En charge")
            self.state_dot.itemconfig(self.state_dot_id, fill=COLORS["accent_green"])

        else:

            self.state_var.set("🔋 Pas en charge")
            self.state_dot.itemconfig(self.state_dot_id, fill=COLORS["accent_orange"])

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
            self.total_seconds = self.remaining_seconds

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

            self.update_timer_display()

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
            self.ring_canvas.itemconfig(self.ring_arc_id, outline=COLORS["accent_red"])

        # --------------------------------------------------
        # SI LE PC N'EST PAS EN CHARGE
        # --------------------------------------------------

        elif self.current_state == "PAS EN CHARGE":

            self.notifier.notify_plug()

            self.status_var.set(
                "⚠ Durée atteinte — rebranchez le chargeur"
            )
            self.ring_canvas.itemconfig(self.ring_arc_id, outline=COLORS["accent_red"])

    # ======================================================
    # AFFICHAGE DU TIMER
    # ======================================================

    def update_timer_display(self):
        """
        Convertit les secondes restantes en HH:MM:SS
        et met à jour le minuteur circulaire.
        """

        hours = self.remaining_seconds // 3600

        minutes = (
            self.remaining_seconds % 3600
        ) // 60

        seconds = self.remaining_seconds % 60

        formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        self.timer_var.set(formatted)

        self.ring_canvas.itemconfig(self.ring_text_id, text=formatted)

        # Fraction du temps restant (1 = plein, 0 = vide).
        if self.total_seconds > 0:
            fraction = self.remaining_seconds / self.total_seconds
        else:
            fraction = 0

        extent = -360 * fraction

        arc_color = COLORS["accent_blue"] if fraction > 0.15 else COLORS["accent_orange"]

        self.ring_canvas.itemconfig(
            self.ring_arc_id, extent=extent, outline=arc_color
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