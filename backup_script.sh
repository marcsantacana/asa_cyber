#!/bin/bash

# Configuració
SOURCE_DIR="/workspaces/asa_cyber/output"
BACKUP_DIR="/workspaces/asa_cyber/backups"
LOG_FILE="/workspaces/asa_cyber/backups/backup.log"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/backup_$DATE.tar.gz"  # Nombre del archivo de respaldo

# Crear directorio de respaldo si no existe
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
fi

# Crear directorio de logs si no existe
LOG_DIR=$(dirname "$LOG_FILE")
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

# Realizar la copia de seguridad
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Iniciando copia de seguridad..." | tee -a "$LOG_FILE"
if tar -czf "$BACKUP_FILE" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"; then
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Copia de seguridad completada: $BACKUP_FILE" | tee -a "$LOG_FILE"
else
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Error al realizar la copia de seguridad." | tee -a "$LOG_FILE"
    exit 1
fi

# Finalización
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Proceso de copia de seguridad finalizado." | tee -a "$LOG_FILE"