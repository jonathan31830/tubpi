"""Interface ONVIF pour piloter la caméra PTZ."""

import os
import logging

try:
    from onvif import ONVIFCamera
except ImportError:  # pragma: no cover
    ONVIFCamera = None

_LOG = logging.getLogger(__name__)

class CameraOnvif:
    def __init__(self, host, port=80, user=None, password=None, motor=None, wsdl_dir=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.motor = motor
        self.wsdl_dir = wsdl_dir
        self.camera = None
        self.media_service = None
        self.ptz_service = None
        self.profile_token = None
        self.connected = False

        self._connect()

    def _default_wsdl_dir(self):
        if ONVIFCamera is None:
            return None
        try:
            import onvif
            return os.path.join(os.path.dirname(onvif.__file__), 'wsdl')
        except Exception:
            return None

    def _connect(self):
        if ONVIFCamera is None:
            _LOG.warning('ONVIF library non disponible. Installation requise: onvif-zeep')
            return

        wsdl_dir = self.wsdl_dir or self._default_wsdl_dir()
        if wsdl_dir is None:
            _LOG.warning('Impossible de localiser le répertoire WSDL ONVIF')
            return

        try:
            self.camera = ONVIFCamera(self.host, self.port, self.user, self.password, wsdl_dir)
            self.media_service = self.camera.create_media_service()
            self.ptz_service = self.camera.create_ptz_service()

            profiles = self.media_service.GetProfiles()
            if profiles:
                self.profile_token = profiles[0].token
            self.connected = True
            _LOG.info('Connexion ONVIF établie avec %s:%s', self.host, self.port)
        except Exception as exc:
            _LOG.warning('Erreur de connexion ONVIF : %s', exc)
            self.connected = False

    def focus_plus(self):
        """Intercepter la commande focus+ pour déplacer le rail vers l'avant."""
        if self.motor is None or not self.motor.is_available():
            raise RuntimeError('Motor driver non disponible')
        self.motor.move_forward()
        return {'action': 'focus_plus', 'motor': 'forward'}

    def focus_minus(self):
        """Intercepter la commande focus- pour déplacer le rail vers l'arrière."""
        if self.motor is None or not self.motor.is_available():
            raise RuntimeError('Motor driver non disponible')
        self.motor.move_backward()
        return {'action': 'focus_minus', 'motor': 'backward'}

    def get_stream_uri(self, protocol='RTSP'):
        """Récupérer l'URI du flux vidéo via le service Media ONVIF."""
        if not self.connected or self.media_service is None:
            raise RuntimeError('Connexion ONVIF non établie')
        request = self.media_service.create_type('GetStreamUri')
        request.StreamSetup = {
            'Stream': 'RTP-Unicast',
            'Transport': {
                'Protocol': protocol
            }
        }
        request.ProfileToken = self.profile_token
        uri = self.media_service.GetStreamUri(request)
        return uri.Uri
