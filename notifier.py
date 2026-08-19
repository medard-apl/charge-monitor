from plyer import notification


class Notifier:
    """
    Classe responsable de l'envoi des notifications
    système.
    """

    def __init__(self, app_name="Charge Monitor"):
        self.app_name = app_name

    def send(self, title, message):
        """
        Envoie une notification système.

        Parameters
        ----------
        title : str
            Titre de la notification.

        message : str
            Contenu de la notification.
        """

        notification.notify(
            title=title,
            message=message,
            app_name=self.app_name,
            timeout=10
        )

    def notify_unplug(self):
        """
        Notification demandant à l'utilisateur
        de débrancher le chargeur.
        """

        self.send(
            "Charge Monitor",
            "Vous êtes en charge depuis la durée définie. "
            "Vous pouvez débrancher votre chargeur."
        )

    def notify_plug(self):
        """
        Notification demandant à l'utilisateur
        de rebrancher le chargeur.
        """

        self.send(
            "Charge Monitor",
            "Vous n'êtes plus en charge depuis la durée définie. "
            "Vous pouvez rebrancher votre chargeur."
        )