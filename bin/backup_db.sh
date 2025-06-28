#!/bin/bash

# Script name: backup_db.sh
# Description: Creates a PostgreSQL database dump

# Determine the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Create backups directory if it doesn't exist
BACKUP_DIR="$PROJECT_ROOT/backups"
mkdir -p "$BACKUP_DIR"

# Load environment variables from the .env file
if [ -f "$PROJECT_ROOT/.env" ]; then
    set -o allexport
    source "$PROJECT_ROOT/.env"
    set +o allexport
elif [ -f "$SCRIPT_DIR/.env" ]; then
    set -o allexport
    source "$SCRIPT_DIR/.env"
    set +o allexport
else
    echo "Error: .env file not found in project root or script directory."
    echo "Current script directory: $SCRIPT_DIR"
    echo "Expected project root: $PROJECT_ROOT"
    exit 1
fi

# Check which database names are available
DB_NAMES=()
if [ ! -z "$POSTGRESQL_DB_NAME" ]; then
    DB_NAMES+=("$POSTGRESQL_DB_NAME")
fi
if [ ! -z "$POSTGRESQL_DB_NAME_WEB" ]; then
    DB_NAMES+=("$POSTGRESQL_DB_NAME_WEB")
fi

if [ ${#DB_NAMES[@]} -eq 0 ]; then
    echo "Error: No database names found in environment variables."
    echo "Please set POSTGRESQL_DB_NAME or POSTGRESQL_DB_NAME_WEB in your .env file."
    exit 1
fi

# Set PostgreSQL connection variables
DB_USER=${POSTGRESQL_DB_USER:-postgres}
DB_PASSWORD=${POSTGRESQL_DB_PASSWORD:-admin}
DB_HOST=${POSTGRESQL_DB_HOST:-db}
DB_PORT=${POSTGRESQL_DB_PORT:-5432}

# Create timestamp for the backup filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Determine if we're using 'docker compose' or 'docker-compose'
if docker compose version &>/dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    echo "Using 'docker compose' command"
elif docker-compose version &>/dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    echo "Using 'docker-compose' command"
else
    echo "Neither 'docker compose' nor 'docker-compose' commands are available"
    exit 1
fi

# Create backup for each database
for DB_NAME in "${DB_NAMES[@]}"; do
    echo "Creating backup for database: $DB_NAME"

    # Generate backup filename
    BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_backup_${TIMESTAMP}.sql"

    # First method: Use docker exec directly with the container name
    echo "Running pg_dump for $DB_NAME using direct container access..."
    docker exec -i postgres pg_dump -U "$DB_USER" -d "$DB_NAME" > "$BACKUP_FILE"

    # Check if backup was successful
    if [ $? -eq 0 ] && [ -s "$BACKUP_FILE" ]; then
        echo "Backup successfully created: $BACKUP_FILE"

        # Create a compressed version
        echo "Compressing backup file..."
        gzip -f "$BACKUP_FILE"
        echo "Compressed backup created: $BACKUP_FILE.gz"

        # Go to next database
        continue
    else
        echo "First backup method failed, trying alternative method..."
        # Remove empty file
        [ -f "$BACKUP_FILE" ] && rm "$BACKUP_FILE"
    fi

    # Alternative method: Use PSQL environment variables and local pg_dump if available
    if command -v pg_dump >/dev/null 2>&1; then
        echo "Trying direct pg_dump access..."
        PGPASSWORD="$DB_PASSWORD" pg_dump -h localhost -p 5432 -U "$DB_USER" -d "$DB_NAME" > "$BACKUP_FILE"

        if [ $? -eq 0 ] && [ -s "$BACKUP_FILE" ]; then
            echo "Backup successfully created: $BACKUP_FILE"

            # Create a compressed version
            echo "Compressing backup file..."
            gzip -f "$BACKUP_FILE"
            echo "Compressed backup created: $BACKUP_FILE.gz"
            continue
        else
            echo "Direct pg_dump failed as well"
            # Remove empty file
            [ -f "$BACKUP_FILE" ] && rm "$BACKUP_FILE"
        fi
    fi

    # If we got here, both methods failed
    echo "Error: Failed to create backup for database $DB_NAME"
done

# List all backups
echo -e "\nAvailable backups:"
ls -lh "$BACKUP_DIR"

# Output total size of backups
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
echo -e "\nTotal backup size: $TOTAL_SIZE"

echo -e "\nBackup process completed at $(date)"