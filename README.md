#  Script de Déploiement Automatique Apache — Nexa

Ce script Python automatise le **déploiement d’un site web local sous Apache**.  
Il crée le site, configure le VirtualHost, vérifie son accessibilité et envoie une notification de réussite via **ntfy.sh**.

---

##  Fonctionnalités

-  Vérifie si **Apache** est actif  
-  Crée un dossier web local (`/Library/WebServer/Documents/nexa`)  
-  Configure un **VirtualHost** (`nexa.local`)  
-  Vérifie l’accès HTTP (`http://nexa.local`)  
-  Envoie une **notification push** via **ntfy.sh**  
-  Génère un **rapport JSON** récapitulatif

---

##  Prérequis

Avant d’exécuter le script, assure-toi que :
- Apache est installé et accessible via `apachectl`
- Tu as les droits administrateur (`sudo`)
- Python 3.x est installé avec les modules :
  ```bash
  pip install requests


	'''
-Rajouter ce domaine à ton fichier /etc/hosts: 
127.0.0.1 nexa.local


## Executer le Script

sudo python3 deploiement.py


 
