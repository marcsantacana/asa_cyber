#!/bin/bash

# Configuració.
SOURCE_DIR="/workspaces/asa_cyber"
BACKUP_DIR="/workspaces/asa_cyber/backups"
LOG_FILE="/workspaces/asa_cyber/backups/backup.log"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/backup_$DATE.tar.gz"

# Crea el directori de còpies de seguretat si no existeix.
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
fi

# Crea la carpeta de logs si no existeix.
LOG_DIR=$(dirname "$LOG_FILE")
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

echo "[$(date +"%Y-%m-%d %H:%M:%S")] Preparant la còpia de seguretat..." | tee -a "$LOG_FILE"
sleep 2
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Analitzant els fitxers i directoris..." | tee -a "$LOG_FILE"
sleep 3
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Començant la compressió dels fitxers..." | tee -a "$LOG_FILE"
sleep 2

# Aquí es realitza la còpia de seguretat.
if tar -czf "$BACKUP_FILE" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"; then
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Copia de seguretat completada: $BACKUP_FILE" | tee -a "$LOG_FILE"
else
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Error al realitzar la còpia de seguretat." | tee -a "$LOG_FILE"
    exit 1
fi

# Imprimir la inalització a l'arxiu de logs.
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Finalitzant el procés de còpia de seguretat..." | tee -a "$LOG_FILE"
sleep 2
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Procés de còpia de seguretat finalitzat." | tee -a "$LOG_FILE"