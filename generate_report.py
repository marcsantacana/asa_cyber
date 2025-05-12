from gophish import Gophish
from gophish.models import *
import openpyxl
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

GOPHISH_URL = os.getenv("GOPHISH_URL")
API_KEY = os.getenv("API_KEY")
VERIFY_SSL = os.getenv("VERIFY_SSL", "False").lower() == "true"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOPHISH_URL or not API_KEY:
    raise ValueError("Cal definir GOPHISH_URL i GOPHISH_API_KEY en el fitxer .env")

api = Gophish(API_KEY, host=GOPHISH_URL, verify=VERIFY_SSL)

# FUNCIONS
def export_excel(summary, filename):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Campanya"

    ws.append(["Campanya", "Emails Enviats", "Emails Oberts", "Clicks", "Submissions"])
    ws.append([
        summary.name,
        summary.stats['emailsSent'],
        summary.stats['opened'],
        summary.stats['clicked'],
        summary.stats['submittedData']
    ])

    wb.save(f"output/{filename}.xlsx")
    print(f"[✔] Exportació Excel feta a output/{filename}.xlsx")

def generate_technical_report(summary, filename):
    with open(f"output/{filename}.txt", "w") as f:
        f.write(f"Informe Tècnic: {summary.name}\n")
        f.write("="*60 + "\n")
        f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write(f"Emails enviats: {summary.stats['emailsSent']}\n")
        f.write(f"Emails oberts: {summary.stats['opened']}\n")
        f.write(f"Enllaços clicats: {summary.stats['clicked']}\n")
        f.write(f"Credencials enviades: {summary.stats['submittedData']}\n")
    print(f"[✔] Informe tècnic generat a output/{filename}.txt")

def generate_gemini_report(summary, filename):
    prompt = f"""
Escriu un informe professional de resultats d'una campanya de phishing educativa. 
La campanya es diu {summary.name}. Es van enviar {summary.stats['emailsSent']} correus.
Es van obrir {summary.stats['opened']}, es van clicar {summary.stats['clicked']} i es van enviar {summary.stats['submittedData']} formularis.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    result = response.json()
    try:
        content = result['candidates'][0]['content']['parts'][0]['text']
        with open(f"output/{filename}_gemini.txt", "w") as f:
            f.write(content)
        print(f"[✔] Informe de Gemini generat a output/{filename}_gemini.txt")
    except Exception as e:
        print("[✖] Error generant l'informe amb Gemini:", e)

def main():
    campaign_id = int(input("🔍 Introdueix l’ID de la campanya a analitzar: "))
    summary = api.campaigns.summary(campaign_id=campaign_id)

    filename = f"campanya_{campaign_id}_{datetime.now().strftime('%Y%m%d_%H%M')}"

    print(" 1. Exportar a Excel")
    print(" 2. Generar informe tècnic")
    print(" 3. Generar informe amb IA (Gemini)")
    choice = input(" Escull una opció (1/2/3): ")

    if choice == '1':
        export_excel(summary, filename)
    elif choice == '2':
        generate_technical_report(summary, filename)
    elif choice == '3':
        generate_gemini_report(summary, filename)
    else:
        print("[✖] Opció no vàlida.")

if __name__ == "__main__":
    main()
