#!/bin/bash
# Database restore script

if [ -z "$1" ]; then
    echo "Usage: ./restore_db.sh <backup_file>"
    echo "Example: ./restore_db.sh backups/backup_20240101_120000.dump"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

# Database configuration
DB_NAME=${DB_NAME:-fabric_erp_db}
DB_USER=${DB_USER:-postgres}

echo "WARNING: This will overwrite the current database!"
read -p "Are you sure you want to continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Restore cancelled."
    exit 1
fi

# Perform restore
pg_restore -U $DB_USER -d $DB_NAME -c -v $BACKUP_FILE

echo "Database restored from: $BACKUP_FILE"