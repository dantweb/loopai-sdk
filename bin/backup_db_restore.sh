#!/bin/bash

# Script name: backup_db_restore.sh
# Description: Restores a PostgreSQL database from a backup file

# Determine the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Backup directory
BACKUP_DIR="$PROJECT_ROOT/backups"

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

# Set PostgreSQL connection variables
DB_USER=${POSTGRESQL_DB_USER:-postgres}
DB_PASSWORD=${POSTGRESQL_DB_PASSWORD:-admin}
DB_HOST=${POSTGRESQL_DB_HOST:-db}
DB_PORT=${POSTGRESQL_DB_PORT:-5432}

# Check if backups directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Error: Backups directory not found: $BACKUP_DIR"
    exit 1
fi

# List available backups
echo "Available backup files:"
BACKUP_FILES=()
i=0

# Find both .sql and .sql.gz files and store them in an array
while IFS= read -r file; do
    if [[ "$file" == *.sql || "$file" == *.sql.gz ]]; then
        BACKUP_FILES+=("$file")
        echo "[$i] $(basename "$file")"
        ((i++))
    fi
done < <(find "$BACKUP_DIR" -type f | sort -r)

# Check if there are any backup files
if [ ${#BACKUP_FILES[@]} -eq 0 ]; then
    echo "No backup files found in $BACKUP_DIR"
    exit 1
fi

# Ask user to select a backup file
echo -e "\nEnter the number of the backup file to restore or 'q' to quit:"
read -r SELECTION

# Check if user wants to quit
if [[ "$SELECTION" == "q" || "$SELECTION" == "Q" ]]; then
    echo "Operation cancelled."
    exit 0
fi

# Validate selection
if ! [[ "$SELECTION" =~ ^[0-9]+$ ]] || [ "$SELECTION" -ge ${#BACKUP_FILES[@]} ]; then
    echo "Invalid selection. Please run the script again and select a valid number."
    exit 1
fi

SELECTED_BACKUP="${BACKUP_FILES[$SELECTION]}"
echo "Selected backup: $(basename "$SELECTED_BACKUP")"

# Determine target database from filename
BACKUP_FILENAME=$(basename "$SELECTED_BACKUP")
DB_NAME=""

# Extract database name from backup filename
if [[ "$BACKUP_FILENAME" =~ ^([^_]+)_backup_ || "$BACKUP_FILENAME" =~ ^([^_]+)_ ]]; then
    DB_NAME="${BASH_REMATCH[1]}"
    echo "Detected database name from filename: $DB_NAME"
else
    # If we couldn't determine the DB name from the filename, ask the user
    echo "Could not determine database name from filename."

    # Display available databases
    echo "Available databases:"

    # Check which database names are available from env vars
    if [ ! -z "$POSTGRESQL_DB_NAME" ]; then
        echo "[1] $POSTGRESQL_DB_NAME"
    fi

    if [ ! -z "$POSTGRESQL_DB_NAME_WEB" ]; then
        echo "[2] $POSTGRESQL_DB_NAME_WEB"
    fi

    echo -e "\nEnter the number of the target database or type the database name:"
    read -r DB_SELECTION

    if [[ "$DB_SELECTION" == "1" && ! -z "$POSTGRESQL_DB_NAME" ]]; then
        DB_NAME="$POSTGRESQL_DB_NAME"
    elif [[ "$DB_SELECTION" == "2" && ! -z "$POSTGRESQL_DB_NAME_WEB" ]]; then
        DB_NAME="$POSTGRESQL_DB_NAME_WEB"
    else
        DB_NAME="$DB_SELECTION"
    fi
fi

# Confirm restore operation
echo -e "\nWARNING: This will overwrite all data in the '$DB_NAME' database!"
echo "Are you sure you want to proceed? (y/n)"
read -r CONFIRM

if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "Operation cancelled."
    exit 0
fi

# Create a timestamp for the pre-restore backup
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
PRE_RESTORE_BACKUP="$BACKUP_DIR/${DB_NAME}_pre_restore_${TIMESTAMP}.sql"

echo "Creating safety backup before restore..."
docker exec -i postgres pg_dump -U "$DB_USER" -d "$DB_NAME" > "$PRE_RESTORE_BACKUP"

if [ $? -eq 0 ] && [ -s "$PRE_RESTORE_BACKUP" ]; then
    echo "Safety backup created: $PRE_RESTORE_BACKUP"
    gzip -f "$PRE_RESTORE_BACKUP"
    echo "Compressed safety backup: $PRE_RESTORE_BACKUP.gz"
else
    echo "Warning: Failed to create safety backup. Do you want to continue anyway? (y/n)"
    read -r CONTINUE
    if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
        echo "Operation cancelled."
        exit 0
    fi
    # Remove empty backup file if it exists
    [ -f "$PRE_RESTORE_BACKUP" ] && rm "$PRE_RESTORE_BACKUP"
fi

# Ask if the user wants to drop the existing database schema before restore
echo -e "\nDo you want to drop all existing tables before restoring? (Recommended) (y/n)"
read -r DROP_TABLES

if [[ "$DROP_TABLES" =~ ^[Yy]$ ]]; then
    echo "Dropping all tables in the database before restore..."

    # Create a temporary script to drop all tables
    DROP_SCRIPT=$(cat <<EOF
DO \$\$
DECLARE
    r RECORD;
BEGIN
    -- Disable all triggers
    EXECUTE 'SET session_replication_role = replica';

    -- Drop all tables in public schema
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;

    -- Drop all sequences
    FOR r IN (SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema = 'public') LOOP
        EXECUTE 'DROP SEQUENCE IF EXISTS public.' || quote_ident(r.sequence_name) || ' CASCADE';
    END LOOP;

    -- Drop all types
    FOR r IN (SELECT typname FROM pg_type t JOIN pg_namespace n ON (t.typnamespace = n.oid)
              WHERE n.nspname = 'public' AND t.typtype = 'c') LOOP
        EXECUTE 'DROP TYPE IF EXISTS public.' || quote_ident(r.typname) || ' CASCADE';
    END LOOP;

    -- Re-enable triggers
    EXECUTE 'SET session_replication_role = DEFAULT';
END \$\$;
EOF
)

    # Execute the drop script
    echo "$DROP_SCRIPT" | docker exec -i postgres psql -U "$DB_USER" -d "$DB_NAME"

    if [ $? -ne 0 ]; then
        echo "Warning: Failed to drop all tables. Restore might fail due to conflicts."
    else
        echo "Successfully dropped all tables in the database."
    fi
fi

# Perform the restore
echo "Restoring database $DB_NAME from backup..."

# Determine if we need to decompress the backup
if [[ "$SELECTED_BACKUP" == *.gz ]]; then
    echo "Restoring from compressed backup..."
    gunzip -c "$SELECTED_BACKUP" | docker exec -i postgres psql -U "$DB_USER" -d "$DB_NAME"
else
    echo "Restoring from uncompressed backup..."
    cat "$SELECTED_BACKUP" | docker exec -i postgres psql -U "$DB_USER" -d "$DB_NAME"
fi

# Check if restore was successful
RESTORE_EXIT_CODE=$?
if [ $RESTORE_EXIT_CODE -eq 0 ]; then
    echo -e "\nDatabase restore completed successfully."
    echo "Database: $DB_NAME"
    echo "Backup file: $SELECTED_BACKUP"
    echo "Restore time: $(date)"
else
    echo -e "\nWarning: Database restore completed with warnings or errors (exit code: $RESTORE_EXIT_CODE)."
    echo "This is often normal when restoring to an existing database, as some objects may already exist."
    echo "Database: $DB_NAME"
    echo "Backup file: $SELECTED_BACKUP"
    echo "Restore time: $(date)"
    echo "If you need to roll back, use the safety backup: $(basename "$PRE_RESTORE_BACKUP.gz")"
fi

# List all backups
echo -e "\nAvailable backups:"
ls -lh "$BACKUP_DIR"

echo -e "\nRestore process completed at $(date)"