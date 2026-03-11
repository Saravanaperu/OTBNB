#!/bin/bash

# Configuration
# Run this from the root directory or configure DATA_DIR path correctly
DATA_DIR="data"
DB_FILE="$DATA_DIR/trading_bot.db"
BACKUP_DIR="$DATA_DIR/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/trading_bot_$TIMESTAMP.db"
MAX_BACKUPS=7

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Check if database exists
if [ ! -f "$DB_FILE" ]; then
    echo "Error: Database file $DB_FILE not found."
    exit 1
fi

echo "Starting database backup..."

# Use sqlite3 .backup command for safe hot backup if sqlite3 is available,
# otherwise fall back to copy
if command -v sqlite3 &> /dev/null; then
    sqlite3 "$DB_FILE" ".backup '$BACKUP_FILE'"
    if [ $? -eq 0 ]; then
        echo "Safe backup completed successfully: $BACKUP_FILE"
    else
        echo "Error: sqlite3 backup failed."
        exit 1
    fi
else
    echo "Warning: sqlite3 not found. Falling back to simple copy."
    cp "$DB_FILE" "$BACKUP_FILE"
    if [ $? -eq 0 ]; then
        echo "Copy backup completed successfully: $BACKUP_FILE"
    else
        echo "Error: Copy backup failed."
        exit 1
    fi
fi

# Cleanup old backups
echo "Cleaning up old backups (keeping last $MAX_BACKUPS)..."
ls -t "$BACKUP_DIR"/trading_bot_*.db | tail -n +$((MAX_BACKUPS + 1)) | xargs -I {} rm -- {} 2>/dev/null || true

echo "Backup process finished."
