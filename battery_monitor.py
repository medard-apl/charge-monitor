import psutil


class BatteryMonitor:
    """
    Classe permettant de récupérer l'état actuel
    de la batterie du PC.
    """

    def __init__(self):
        """
        Initialise le moniteur.
        """

        # Dernier état connu de la batterie.
        self.previous_state = None

    def is_charging(self):
        """
        Retourne True si le PC est actuellement branché
        au secteur.

        Retourne False s'il fonctionne sur batterie.
        """

        battery = psutil.sensors_battery()

        # Certains ordinateurs peuvent ne pas fournir
        # les informations relatives à la batterie.
        if battery is None:
            return None

        return battery.power_plugged

    def get_state(self):
        """
        Retourne une chaîne représentant l'état actuel.
        """

        charging = self.is_charging()

        if charging is None:
            return "INCONNU"

        if charging:
            return "EN CHARGE"

        return "PAS EN CHARGE"
    def get_percentage(self):
        """
        Retourne le pourcentage actuel de batterie.
        """

        battery = psutil.sensors_battery()

        if battery is None:
            return None

        return battery.percent