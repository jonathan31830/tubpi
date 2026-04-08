"""Pilote du moteur pour le déplacement de la caméra sur rail."""

class MotorDriver:
    def __init__(self, enable_pin=None, forward_pin=None, backward_pin=None):
        self.enable_pin = enable_pin
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin
        # TODO: initialiser les GPIO

    def move_forward(self, speed=50):
        """Démarrer le déplacement vers l'avant."""
        raise NotImplementedError

    def move_backward(self, speed=50):
        """Démarrer le déplacement vers l'arrière."""
        raise NotImplementedError

    def stop(self):
        """Arrêter le moteur."""
        raise NotImplementedError

    def calibrate(self):
        """Calibrer la position de référence du rail."""
        raise NotImplementedError
