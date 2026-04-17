# Matériel requis

## Raspberry Pi
- Raspberry Pi 5 recommandé
- Alternative : Raspberry Pi 3B si besoin, mais privilégier le Pi 5 pour les performances et la compatibilité.

## Motorisation
- Carte `RPI Motor Driver Board`
- Moteur DC ou moteur pas à pas compatible avec le rail
- Alimentation moteur 12V ou 24V selon le moteur
- RPi Motor Driver Board

Raspberry Pi Expansion Board, DC Motor / Stepper Motor Driver
### Introduction

Interface definitions
Interface	wiringPi	BCM
M1	        P28	        20
M2	        P29	        21
PWMA	    P25	        26
M3	        P22 	    6
M4	        P23	        13
PWMB	    P26	        12

M1 and M2 are connected to the right motor, while M3 and M4 are connected to the left motor. PWMA and PWMB are output enable pins, active high enable. When they are driven to high level, the PWM pulse will be outputted from M1, M2, M3 and M4, so as to control the speed of the robot.

Control work
M1	M2	M3	M4	Descriptions
1	0	1	0	When the motors rotate forwards, the robot goes straight
0	1	0	1	When the motors rotate backwards, the robot draws back
0	0	1	0	When the right motor stops and left motor rotates forwards, the robot turns right
1	0	0	0	When the left motor stops and right motor rotates forwards, the robot turns left
0	0	0	0	When the motors stop, the robot stops


## Capteurs
- Capteurs de fin de course pour chaque extrémité du rail
- Capteurs de position ou encodeur pour mesurer le déplacement

## Caméra
- Caméra IP PTZ ONVIF (par exemple Dahua)
- Connexion réseau fiable pour le flux vidéo et les commandes

## Mécanique
- Rail solide adapté au poids de la caméra
- Supports de fixation
- Système de transmission : courroie, pignon ou engrenage
- Châssis rigide pour limiter les vibrations
