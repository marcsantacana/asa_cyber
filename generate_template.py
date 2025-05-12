import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning

# Carregar la clau d'API des del fitxer .env
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Endpoint del model Gemini 2.0 Flash
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def generar_contingut(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(GEMINI_ENDPOINT, headers=headers, data=json.dumps(body))

    if response.status_code != 200:
        raise Exception(f"Error en la resposta de l'API Gemini: {response.status_code} - {response.text}")

    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise ValueError("No s'ha pogut obtenir el contingut generat")

def generar_correu(nom_usuari):
    prompt = f"""
    Escriu un correu electrònic de phishing en català per a un usuari anomenat {nom_usuari}, 
    simulant ser un missatge de LinkedIn, on s'indiqui que el compte ha estat bloquejat 
    i que cal actualitzar la contrasenya fent clic en un enllaç. Sigues convincent, breu i formal.
    """
    return generar_contingut(prompt)

def generar_html():
    prompt = """
    Genera una pàgina HTML de phishing que simuli ser l'inici de sessió de LinkedIn. 
    Ha d'incloure camps per a correu electrònic i contrasenya, i un botó de \"Inicia sessió\".
    Estil simple i responsive.
    """
    return generar_contingut(prompt)

def guardar_fitxer(contingut, directori, nom_arxiu):
    os.makedirs(directori, exist_ok=True)
    path = os.path.join(directori, nom_arxiu)
    with open(path, "w", encoding="utf-8") as f:
        f.write(contingut)
    print(f"Fitxer guardat: {path}")

def main():
    if not API_KEY:
        raise ValueError("Cal definir GOOGLE_API_KEY en l'entorn o .env")

    nom_usuari = "Joan"
    correu_text = generar_correu(nom_usuari)
    html_text = generar_html()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = f"output/generacio_{timestamp}"

    guardar_fitxer(correu_text, base_dir, "correu.txt")
    guardar_fitxer(html_text, base_dir, "plantilla.html")

if __name__ == "__main__":
    main()