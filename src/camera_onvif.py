"""Interface ONVIF pour piloter la caméra PTZ."""

class CameraOnvif:
    def __init__(self, host, port=80, user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        # TODO: initialiser la connexion ONVIF

    def focus_plus(self):
        """Intercepter la commande focus+ pour déplacer la caméra."""
        raise NotImplementedError

    def focus_minus(self):
        """Intercepter la commande focus- pour déplacer la caméra."""
        raise NotImplementedError

    def get_stream_uri(self):
        """Récupérer l'URI du flux vidéo."""
        raise NotImplementedError
