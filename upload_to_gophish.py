import os
import json
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from gophish import Gophish

load_dotenv()

GOPHISH_URL = os.getenv("GOPHISH_URL")
API_KEY = os.getenv("API_KEY")

if not GOPHISH_URL or not API_KEY:
    raise ValueError("Cal definir GOPHISH_URL i GOPHISH_API_KEY en el fitxer .env")

API_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Ruta de l'última generació de contingut
output_base = "output/generacio_20250507_214535"

# Comprovar que el directori existeix
if not os.path.isdir(output_base):
    raise NotADirectoryError(f"No s'ha trobat el directori: {output_base}")

# Construir les rutes dels fitxers
correu_path = os.path.join(output_base, "correu.txt")
html_path = os.path.join(output_base, "plantilla.html")

# Comprovar que els fitxers existeixen
if not os.path.isfile(correu_path):
    raise FileNotFoundError(f"No s'ha trobat el fitxer: {correu_path}")
if not os.path.isfile(html_path):
    raise FileNotFoundError(f"No s'ha trobat el fitxer: {html_path}")

# Llegir fitxers generats
with open(correu_path, "r", encoding="utf-8") as f:
    email_body = f.read()

with open(html_path, "r", encoding="utf-8") as f:
    landing_html = f.read()

# Timestamp per a noms únics
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# 1. Crear plantilla de correu electrònic
template_data = {
    "name": f"Plantilla_LinkedIn_{timestamp}",
    "subject": "El teu compte de LinkedIn ha estat bloquejat",
    "text": email_body,
    "html": "",  # Si vols fer servir HTML també, el pots afegir aquí
    "type": "email"
}
template_response = requests.post(f"{GOPHISH_URL}/api/templates/", headers=API_HEADERS, json=template_data)
template_response.raise_for_status()
template_id = template_response.json()["id"]
print(f"[✔] Plantilla creada: ID {template_id}")

# 2. Crear landing page
landing_data = {
    "name": f"Landing_LinkedIn_{timestamp}",
    "html": landing_html,
    "capture_credentials": True,
    "capture_passwords": True,
    "redirect_url": "https://www.linkedin.com"
}
landing_response = requests.post(f"{GOPHISH_URL}/api/landing_pages/", headers=API_HEADERS, json=landing_data)
landing_response.raise_for_status()
landing_id = landing_response.json()["id"]
print(f"[✔] Landing page creada: ID {landing_id}")

# 3. Crear grup de destinataris de prova
group_data = {
    "name": f"Grup_de_prova_{timestamp}",
    "targets": [
        {"first_name": "Joan", "last_name": "Prova", "email": "joan@enti.cat"},
        {"first_name": "Anna", "last_name": "Test", "email": "anna@enti.cat"}
    ]
}
group_response = requests.post(f"{GOPHISH_URL}/api/groups/", headers=API_HEADERS, json=group_data)
group_response.raise_for_status()
group_id = group_response.json()["id"]
print(f"[✔] Grup de prova creat: ID {group_id}")

# 4. Crear la campanya
campaign_data = {
    "name": f"Campanya_LinkedIn_{timestamp}",
    "template": {"id": template_id},
    "url": "http://tu-servidor.local",  # Canvia aquest valor segons la teva configuració de túnel
    "landing_page": {"id": landing_id},
    "groups": [{"id": group_id}],
    "smtp": {"id": 1},  # Assegura't que tens un servidor SMTP amb ID 1 configurat
    "launch_date": "",  # En blanc per llançar-la immediatament
    "send_by_date": ""
}
campaign_response = requests.post(f"{GOPHISH_URL}/campaigns/", headers=API_HEADERS, json=campaign_data)
campaign_response.raise_for_status()
campaign_id = campaign_response.json()["id"]
print(f"[✔] Campanya creada i llançada: ID {campaign_id}")
