# Tubpi - Caméra sur rail pilotée par Raspberry Pi 5

## Objectif
Développer un système permettant de déplacer automatiquement une caméra sur un rail à l'aide d'un Raspberry Pi 5 et d'une caméra PTZ ONVIF.

## Besoin
- Déplacer la caméra le long d'un rail avec commande avant/arrière.
- Prendre en charge les commandes ONVIF PTZ focus+ / focus- pour piloter le déplacement.
- Offrir une interface de commande locale ou web.
- Assurer la sécurité avec des capteurs de fin de course et l'arrêt d'urgence.

## Matériel principal
- Raspberry Pi 5
- Carte `RPI Motor Driver Board`
- Moteur DC ou moteur pas à pas adapté au rail
- Capteurs de fin de course ou capteurs de position
- Caméra IP PTZ ONVIF (Dahua ou équivalent)
- Alimentation stable pour le Pi et le moteur
- Châssis / rail, supports, courroie ou engrenages

## Structure du projet
- `plan.md` : plan de développement et besoins
- `README.md` : présentation globale du projet
- `requirements.txt` : dépendances Python
- `src/` : code source du projet
- `docs/` : documentation matériel et architecture

## Démarrage
1. Installer l'OS sur le Raspberry Pi 5.
2. Installer les dépendances Python via `pip install -r requirements.txt`.
3. Vérifier les connexions du moteur et des capteurs.
4. Lancer le serveur web avec `python src/web_app.py`.

## Améliorations futures
- Programmation de trajectoires automatiques.
- Suivi d'objet et mode automatique.
- Application mobile ou API RESTful avancée.
