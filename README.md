# Cisco-Showroom-RoomControl
Real-Life example on how to handle RoomControl capabilities on Cisco CE8+ Video Endpoints (MS, SX ...)

## Généralités

La fonctionnalité « Room Control » est disponible sur l’ensemble des terminaux vidéo Cisco depuis la version CE8.1. Elle permet de personnaliser certaines interfaces de la dalle tactile Touch 10, et offre des API permettant à l’utilisateur d’interagir (de façon bidirectionnelle) avec des systèmes tiers (éclairage,…).

L’interface web des codecs offre une nouvelle option permettant la personnalisation de la dalle Touch 10 en mode WYSIWYG.

![Image](https://github.com/gbraux/Cisco-Showroom-RoomControl/raw/master/Screenshots/ShowroomLayout.PNG)
![Image](https://github.com/gbraux/Cisco-Showroom-RoomControl/raw/master/Screenshots/Room_Control_Screenshot.png)

Dans ce code d'exemple, implémenté dans le Showroom Cisco Collaboration France, les systèmes tiers contrôlables à ce jour sont :
- Lampadaire halogène de la salle Monet
- Store occultant électrique de la salle Van Gogh
- Matrice Vidéo Kramer

## Architecture

### Codecs

Les codecs impliqués (Monet et VanGogh) ont la charge de présenter le menu « Room Control » auprès de l’utilisateur. Ils n’interagissent pas directement avec les dispositifs à contrôler.

Chaque action de l’utilisateur sur l’interface tactile génère un évènement (http) qui sera capturé par le middleware de contrôle du showroom. Inversement, l’API du codec offre la capacité au middleware (toujours via http) de modifier en temps réel certains états de l’interface tactile (état d’un bouton, texte …).

### Middleware de contrôle

Le middleware de contrôle (RoomControlHandler.py) est le lien entre le codec et les éléments à piloter. Il interprète les évènements du codec (« bouton appuyé ») et les traduit en ordre (ou suite d’ordres) compréhensibles par les dispositifs à piloter.

Il s’agit d’une application Python 3.5 (non compatible Python 2.x) active sur un serveur quelconque (Windows ou Linux).

Pour windows, cette application est enregistrée en tant que service windows « room_control » (via l’application nssm.exe) lui permettant de démarrer automatiquement au démarrage du serveur (sans nécessiter l’ouverture d’une session).

![Image](https://github.com/gbraux/Cisco-Showroom-RoomControl/raw/master/Screenshots/NSSM_Screenshot.png)

Le middleware agit de la façon suivante :

1.	Immédiatement après le démarrage, l’application s’enregistre (HTTP POST) auprès de l’API de gestion d’évènement du/des codecs. Cela donne l’ordre au(x) codec(s) de transmettre l’ensemble des évènements UX au middleware sur le port 1412.

2.	Le middleware se met en écoute sur le port 1412 et attends les évènements du/des codecs.

3.	En cas de réception d’un évènement, le middleware détermine si il s’agit d’un évènements à gérer ou non, et prends les actions nécessaires. Lorsque le middleware écoute des évènements de plusieurs codecs, l’adresse MAC présenté dans le message de l’évènement est utilisée pour en identifier la source.

4.	Toutes les minutes, le middleware renouvelle son enregistrement auprès l’API de gestion d’évènement du/des codecs (pour gérer, par exemple, un reboot du codec).

5.	Toutes les minutes également, le middleware synchronise l’état des systèmes contrôlés (état des lumières, …) pour que l’état du bouton associé sur la dalle Touch 10 soit cohérent avec l’état réel du système.

### Systemes controlés

La commutation on/off des systèmes est réalisée par des Relais IP KMTronic 2 canaux : http://kmtronic.com/km-web-two-relay-box.html.

![Image](https://raw.githubusercontent.com/gbraux/Cisco-Showroom-RoomControl/master/Screenshots/relay_screenshot.jpg)

Ces relais sont connectés (RJ45) sur le réseau, et disposent d’une API HTTP. L’API permet de changer les états des relais, mais aussi d’obtenir l’état courant (ouvert/fermé).

Pour le contrôle de l’éclairage halogène de la salle Monet, le relais est positionné dans le faux-plancher. Il est en coupure sur le câble électrique CE qui alimente l’éclairage, et seul 1 canal est utilisé.

Pour le contrôle du store électrique de la salle Van Gogh, le relais est positionné dans le faux-plancher (baie technique) dans une boite Plexo. Il est en parallèle des 2 fils pilotes du store (monté, descente + commun). Les 2 canaux sont utilisé (monté / descente du store)

Le middleware implémente l’API des relais dans une Classe Python réutilisable.
