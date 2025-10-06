import os
import subprocess
import logging
import requests
import json
import time

# --- CONFIG ---
VHOST_NAME = "nexa.local"
DOC_ROOT = "/Library/WebServer/Documents/nexa"
LOG_FILE = "deploiement.log"
NTFY_TOPIC = "hendrix"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"

# --- LOGGING ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- FONCTIONS ---
def check_apache():
    """Vérifie si Apache tourne"""
    try:
        result = subprocess.run(["sudo", "apachectl", "status"], capture_output=True, text=True)
        logger.info("Apache est en cours d'exécution ✅")
        return True
    except Exception as e:
        logger.error(f"Apache n'est pas accessible : {e}")
        return False

def create_site():
    """Crée le dossier du site et index.html"""
    try:
        os.makedirs(DOC_ROOT, exist_ok=True)
        index_file = os.path.join(DOC_ROOT, "index.html")
        with open(index_file, "w") as f:
            f.write("<html><head><title>hello nexa</title></head><body>Hello Nexa!</body></html>")
        logger.info(f"Dossier site créé et index.html ajouté : {DOC_ROOT}")
        return True
    except Exception as e:
        logger.error(f"Erreur création site : {e}")
        return False

def configure_vhost():
    """Configure le virtual host dans Apache"""
    try:
        vhost_conf = f"""
<VirtualHost *:80>
    ServerName {VHOST_NAME}
    DocumentRoot "{DOC_ROOT}"
    <Directory "{DOC_ROOT}">
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
"""
        conf_path = "/etc/apache2/extra/httpd-vhosts.conf"
        with open(conf_path, "a") as f:
            f.write(vhost_conf)
        logger.info(f"Virtual host ajouté à {conf_path}")
        subprocess.run(["sudo", "apachectl", "restart"], check=True)
        logger.info("Apache redémarré avec la nouvelle configuration ✅")
        return True
    except Exception as e:
        logger.error(f"Erreur config virtual host : {e}")
        return False

def check_http():
    """Vérifie que http://nexa.local répond avec code 200"""
    try:
        response = requests.get(f"http://{VHOST_NAME}")
        logger.info(f"Réponse HTTP: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Erreur HTTP request : {e}")
        return False

def send_ntfy(success):
    """Envoie une notification via ntfy"""
    message = "Déploiement Apache réussi " if success else "Échec du déploiement Apache "
    try:
        requests.post(NTFY_URL, data=message.encode("utf-8"), headers={"Title": "Déploiement Nexa"})
        logger.info("Notification envoyée via ntfy")
        return True
    except Exception as e:
        logger.error(f"Erreur notification ntfy : {e}")
        return False

# --- SCRIPT PRINCIPAL ---
report = {
    "apache_running": False,
    "site_created": False,
    "vhost_configured": False,
    "http_200": False,
    "notification_sent": False
}

# 1. Vérifier Apache
report["apache_running"] = check_apache()

# 2. Créer site
if report["apache_running"]:
    report["site_created"] = create_site()
    report["vhost_configured"] = configure_vhost()

# 3. Vérifier HTTP
if report["site_created"] and report["vhost_configured"]:
    time.sleep(2)  # laisser Apache redémarrer
    report["http_200"] = check_http()

# 4. Notification ntfy
report["notification_sent"] = send_ntfy(
    report["apache_running"] and report["site_created"] and report["vhost_configured"] and report["http_200"]
)

# 5. Affichage JSON final
print(json.dumps(report, indent=4))
