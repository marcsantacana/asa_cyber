import subprocess
import sys

def executar(script):
    try:
        print(f"\nExecutant: {script}...\n")
        subprocess.run([sys.executable, script], check=True)
    except subprocess.CalledProcessError:
        print(f"Error en executar {script}.")

def executar_bash(script):
    try:
        print(f"\nExecutant script bash: {script}...\n")
        subprocess.run(["bash", script], check=True)
    except subprocess.CalledProcessError:
        print(f"Error en executar {script}.")

def mostrar_menu():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Generar informe")
        print("2. Generar plantilla")
        print("3. Pujar plantilla a Gophish")
        print("4. Fer còpia de seguretat")
        print("5. Executar tot el procés")
        print("0. Sortir")

        opcio = input("Selecciona una opció: ")

        if opcio == "1":
            executar("generate_report.py")
        elif opcio == "2":
            executar("generate_template.py")
        elif opcio == "3":
            executar("upload_to_gophish.py")
        elif opcio == "4":
            executar_bash("backup_script.sh")
        elif opcio == "5":
            executar("generate_template.py")
            executar("upload_to_gophish.py")
            executar("generate_report.py")
            executar_bash("backup_script.sh")
        elif opcio == "0":
            print("Sortint...")
            break
        else:
            print("Opció no vàlida. Torna-ho a provar.")

if __name__ == "__main__":
    mostrar_menu()
