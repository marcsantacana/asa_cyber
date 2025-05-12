import requests
import json
from datetime import datetime

API_KEY = "LA_TEVA_API_KEY"
API_URL = "https://IP_DEL_SERVIDOR_GOPHISH/api/campaigns/"
HEADERS = {"Authorization": API_KEY}

def get_campaign_data(campaign_id):
    response = requests.get(f"{API_URL}{campaign_id}?expand=true", headers=HEADERS)
    return response.json()

def generate_report(campaign_data):
    name = campaign_data['name']
    results = campaign_data['results']
    stats = campaign_data['stats']
    
    report = f"""
    Informe de Campanya de Phishing
    -------------------------------
    Nom de la Campanya: {name}
    Data d'Inici: {campaign_data['launch_date']}
    Total Enviats: {stats['total']}
    Correus Oberts: {stats['opened']}
    Clics a l'enllaç: {stats['clicked']}
    Enviaments de Credencials: {stats['submitted_data']}
    Percentatge de Victimes: {stats['success_rate']}%
    """
    filename = f"informe_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write(report)
    print(f"Informe generat: {filename}")

# Exemple d'ús
campaign_id = 1
data = get_campaign_data(campaign_id)
generate_report(data)
