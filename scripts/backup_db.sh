#!/bin/bash
# Database backup script

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Database configuration
DB_NAME=${DB_NAME:-fabric_erp_db}
DB_USER=${DB_USER:-postgres}

# Perform backup
pg_dump -U $DB_USER -d $DB_NAME -F c -b -v -f "$BACKUP_DIR/backup_$TIMESTAMP.dump"

echo "Backup created: $BACKUP_DIR/backup_$TIMESTAMP.dump"
echo "Backup size: $(du -h "$BACKUP_DIR/backup_$TIMESTAMP.dump" | cut -f1)"