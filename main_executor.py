import os
import subprocess

def execute_file(file_name):
    try:
        subprocess.run(["python", file_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing {file_name}: {e}")

if __name__ == "__main__":
    # Lista de archivos Python con sus nombres reales
    files_to_execute = ["generate_template.py", "upload_to_gophish.py", "generate_report.py"]

    print("Seleccione el archivo que desea ejecutar:")
    for i, file in enumerate(files_to_execute, start=1):
        print(f"{i}. {file}")

    try:
        choice = int(input("Ingrese el número correspondiente: "))
        if 1 <= choice <= len(files_to_execute):
            execute_file(files_to_execute[choice - 1])
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
    except ValueError:
        print("Entrada no válida. Por favor, ingrese un número.")