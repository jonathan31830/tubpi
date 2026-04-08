# Architecture logicielle

## Objectifs logiciels
- Piloter le moteur du rail depuis le Raspberry Pi
- Intercepter les commandes ONVIF focus+ / focus- pour les mapper au mouvement du rail
- Proposer une interface de contrôle local ou web
- Assurer des arrêts d'urgence et la gestion des limites

## Modules principaux
- `src/motor_driver.py` : gestion du pilote moteur et des commandes de déplacement
- `src/camera_onvif.py` : gestion de la caméra ONVIF et des commandes PTZ
- `src/web_app.py` : interface web simple pour commander le rail

## Flux de données
1. Le client envoie une commande via l’interface web ou déclenche un événement ONVIF.
2. Le module ONVIF traduit la commande focus+ / focus- en instruction de mouvement.
3. Le moteur est actionné dans la bonne direction et à la bonne vitesse.
4. Les capteurs de fin de course ou de position valident les limites de déplacement.
5. Le serveur renvoie l’état et les erreurs éventuelles.
