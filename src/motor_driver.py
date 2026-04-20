"""Pilote du moteur pour le déplacement de la caméra sur rail."""

import sys
import time
import threading
import RPi.GPIO as GPIO

class MotorDriver:
    # Ramp configuration
    PWM_FREQ = 1000        # Hz
    RAMP_STEPS = 20        # number of steps 0 → 100 %
    RAMP_STEP_DELAY = 0.02 # seconds between steps (~0.4 s total ramp time)

    def __init__(self, forward_pin=20, backward_pin=21, pwm_pin=26):
        print("Initialiser les GPIO")
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin
        self._pwm_pin = pwm_pin
        self._pwm = None
        self._duty = 0          # current duty cycle (0-100)
        self._current_fwd = False   # current forward pin state
        self._current_bwd = False   # current backward pin state
        self._lock = threading.Lock()   # serializes commands
        self._cancel = threading.Event()  # signals ramp loops to stop early
        self.enabled = False

        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.forward_pin, GPIO.OUT)
            GPIO.setup(self.backward_pin, GPIO.OUT)
            GPIO.setup(self._pwm_pin, GPIO.OUT)

            self._pwm = GPIO.PWM(self._pwm_pin, self.PWM_FREQ)
            self._pwm.start(0)

            GPIO.output(self.forward_pin, GPIO.LOW)
            GPIO.output(self.backward_pin, GPIO.LOW)
            self._current_fwd = GPIO.LOW
            self._current_bwd = GPIO.LOW
            self.enabled = True
        except RuntimeError as exc:
            print(f"Impossible d'initialiser les GPIO : {exc}")
            self.enabled = False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _set_direction(self, fwd, bwd):
        GPIO.output(self.forward_pin, fwd)
        GPIO.output(self.backward_pin, bwd)
        self._current_fwd = fwd
        self._current_bwd = bwd

    def _ramp_up(self):
        """Increase duty cycle to 100 %, stopping early if cancelled."""
        step = max(1, int((100 - self._duty) / self.RAMP_STEPS))
        duty = self._duty
        while duty < 100 and not self._cancel.is_set():
            duty = min(duty + step, 100)
            self._pwm.ChangeDutyCycle(duty)
            self._duty = duty
            time.sleep(self.RAMP_STEP_DELAY)

    def _ramp_down(self):
        """Decrease duty cycle to 0 %, stopping early if cancelled."""
        step = max(1, int(self._duty / self.RAMP_STEPS))
        duty = self._duty
        while duty > 0 and not self._cancel.is_set():
            duty = max(duty - step, 0)
            self._pwm.ChangeDutyCycle(duty)
            self._duty = duty
            time.sleep(self.RAMP_STEP_DELAY)

    def _execute(self, fwd, bwd, do_move):
        """
        Interrupt any running ramp, acquire the lock, then:
          1. Check if already moving in the requested direction
          2. If not, ramp down to 0
          3. Switch direction
          4. Ramp up (if do_move=True)
        """
        self._cancel.set()          # interrupt running ramp immediately
        with self._lock:
            self._cancel.clear()    # we now own the motor
            
            # Check if already moving in the requested direction at full speed
            if do_move and fwd == self._current_fwd and bwd == self._current_bwd and self._duty == 100:
                # Already at full speed in the correct direction, nothing to do
                return
            
            self._ramp_down()
            if self._cancel.is_set():
                return              # superseded by yet another command
            self._set_direction(fwd, bwd)
            if do_move:
                self._ramp_up()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def move_forward(self):
        """Démarrer le déplacement vers l'avant avec accélération progressive."""
        if not self.enabled:
            raise RuntimeError('GPIO non disponible')
        self._execute(GPIO.HIGH, GPIO.LOW, do_move=True)

    def move_backward(self):
        """Démarrer le déplacement vers l'arrière avec accélération progressive."""
        if not self.enabled:
            raise RuntimeError('GPIO non disponible')
        self._execute(GPIO.LOW, GPIO.HIGH, do_move=True)

    def stop(self):
        """Arrêter le moteur avec décélération progressive."""
        if not self.enabled:
            return
        self._execute(GPIO.LOW, GPIO.LOW, do_move=False)

    def calibrate(self):
        """Calibrer la position de référence du rail."""
        self.stop()
        return {'message': 'calibration automatique non implémentée'}

    def cleanup(self):
        """Libérer les GPIO."""
        if not self.enabled:
            return
        self.stop()
        if self._pwm:
            self._pwm.stop()
            self._pwm = None  # Prevent double cleanup in __del__
        GPIO.cleanup()
        self.enabled = False

    def is_available(self):
        return self.enabled

    def check_gpio(self):
        """Vérifie si les GPIO ont été initialisés correctement."""
        return self.is_available()

    def run_test_sequence(self):
        """Exécute un test moteur : gauche 10s, droite 10s, arrêt."""
        if not self.enabled:
            raise RuntimeError('GPIO non disponible')

        print('Test moteur : aller gauche 10 secondes')
        self.move_backward()
        time.sleep(10)

        print('Test moteur : aller droit 10 secondes')
        self.move_forward()
        time.sleep(10)

        print('Arrêt du moteur')
        self.stop()


if __name__ == '__main__':
    driver = MotorDriver()
    if driver.is_available():
        if len(sys.argv) > 1 and sys.argv[1] == 'test':
            driver.run_test_sequence()
            driver.cleanup()
        else:
            print('GPIO disponible : initialisation réussie.')
            driver.cleanup()
    else:
        print('GPIO non disponible : vérifiez que le programme est exécuté sur un Raspberry Pi avec accès aux GPIO.')
