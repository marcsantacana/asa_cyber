import requests
import json
import time

# Carregar configuració
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

GOPHISH_URL = config['gophish_url']
API_KEY = config['api_key']

# Funció per crear una nova campanya
def create_campaign():
    url = f'{GOPHISH_URL}/api/campaigns/'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
    }
    payload = {
        'name': 'Campanya de Phishing',
        'from_address': 'noreply@phishing.com',
        'subject': 'Urgent! Actualitza les teves dades.',
        'template': 1,  # Assegura't d'utilitzar l'ID de la plantilla correcta
        'group': 1,     # Utilitza l'ID del grup d'usuaris
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Campanya creada correctament!")
    else:
        print(f"Error al crear la campanya: {response.text}")

# Funció per obtenir els resultats de la campanya
def get_campaign_results(campaign_id):
    url = f'{GOPHISH_URL}/api/campaigns/results/{campaign_id}'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        results = response.json()
        return results
    else:
        print(f"Error al obtenir els resultats: {response.text}")
        return []

# Execució del procés
if __name__ == '__main__':
    create_campaign()
    time.sleep(10)  # Espera que la campanya s'hagi llançat
    campaign_id = 1  # Canvia per l'ID de la campanya real
    results = get_campaign_results(campaign_id)
    print(results)
