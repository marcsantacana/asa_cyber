from gophish import Gophish
from gophish.models import Campaign
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import openpyxl
from openpyxl.styles import Font
import requests
import json

# CONFIGURACIÓ
API_KEY = '7c68e492db6b206a7852b247eb280109ef489470cfec5eb54b6c42489edae1ef'
GOPHISH_HOST = 'https://127.0.0.1:3333/'
VERIFY_SSL = False
GEMINI_API_KEY = 'AIzaSyAdACe-iEGNAdgfjFHiKpzeM4a26KaeRuk'

api = Gophish(API_KEY, host=GOPHISH_HOST, verify=VERIFY_SSL)

def obtenir_campanya():
    campanyes = api.campaigns.get()
    for c in campanyes:
        print(f"[{c.id}] {c.name}")
    id_campanya = int(input("\nIntrodueix l’ID de la campanya: "))
    return api.campaigns.get(id_campanya, expand=True)

def exportar_excel(campanya):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resultats Phishing"

    capsaleres = ['Nom', 'Email', 'Estat', 'Hora']
    ws.append(capsaleres)

    for r in ws[1]:
        r.font = Font(bold=True)

    for result in campanya.results:
        nom = result.first_name or "-"
        email = result.email or "-"
        status = result.status or "Sense dades"
        hora = result.reported or "-"
        ws.append([nom, email, status, hora])

    fitxer = f"campanya_{campanya.id}_resultats.xlsx"
    wb.save(fitxer)
    print(f"[✓] Arxiu Excel exportat com: {fitxer}")

def generar_grafic(stats, fitxer):
    labels = ['Enviats', 'Oberts', 'Clicats', 'Credencials Enviades']
    valors = [stats['total'], stats['opened'], stats['clicked'], stats['submitted_data']]
    plt.figure(figsize=(6,6))
    plt.pie(valors, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title("Estadístiques de la Campanya")
    plt.savefig(fitxer)
    plt.close()

def generar_pdf(campanya):
    stats = campanya.stats
    nom = campanya.name
    data_inici = campanya.launch_date
    data_fi = getattr(campanya, 'completed_date', 'En procés')

    graf = f"graf_{nom}.png"
    generar_grafic(stats, graf)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Informe Tècnic: {nom}", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Inici: {data_inici}", ln=True)
    pdf.cell(200, 10, f"Finalització: {data_fi}", ln=True)
    for k, v in stats.items():
        pdf.cell(200, 10, f"{k.capitalize()}: {v}", ln=True)

    pdf.ln(10)
    pdf.image(graf, x=35, w=140)

    fitxer = f"informe_{nom}_{datetime.now().strftime('%Y%m%d')}.pdf"
    pdf.output(fitxer)
    print(f"[✓] Informe PDF generat: {fitxer}")

def generar_resum_amb_gemini(campanya):
    resum_text = f"""
Campanya: {campanya.name}
Data: {campanya.launch_date}
Estadístiques: {campanya.stats}
Destinataris: {[r.email for r in campanya.results]}
Quines conclusions es poden extreure d’aquesta campanya de phishing?
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": resum_text}]
        }]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    resultat = response.json()

    try:
        text = resultat['candidates'][0]['content']['parts'][0]['text']
        print("\n🧠 Informe analític generat per Gemini:\n")
        print(text)
        return text
    except Exception as e:
        print(f"[!] Error amb la resposta de Gemini: {e}")

def menu():
    campanya = obtenir_campanya()
    print("\nOpcions disponibles:")
    print("1. Exportar resultats a Excel (.xlsx)")
    print("2. Generar informe tècnic (PDF)")
    print("3. Generar resum amb IA (Gemini)")

    opcio = input("\nSelecciona una opció (1/2/3): ").strip()

    if opcio == "1":
        exportar_excel(campanya)
    elif opcio == "2":
        generar_pdf(campanya)
    elif opcio == "3":
        generar_resum_amb_gemini(campanya)
    else:
        print("Opció no vàlida.")

if __name__ == "__main__":
    menu()
