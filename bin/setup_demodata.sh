#!/bin/bash

# -------------------------------------------------------------------
# Script: setup_demodata.sh
# Description: Imports a PostgreSQL database dump from ./var/demodata/dump.sql
#              into the specified database using Docker Compose.
# IMPORTANT: run it once. run it from the /app inside loopai_eb container
# -------------------------------------------------------------------

# Exit immediately if a command exits with a non-zero status
set -e

# Enable debug mode (optional: uncomment for troubleshooting)
# set -x

# Load environment variables from the .env file
echo "Loading environment variables from .env ..."
set -o allexport
source .env
set +o allexport

# Function to display error messages
function error_exit {
    echo "Error: $1" >&2
    exit 1
}

# Check if the required environment variable POSTGRESQL_DB_NAME is set
if [ -z "$POSTGRESQL_DB_NAME" ]; then
    error_exit "POSTGRESQL_DB_NAME is not set in the .env file."
fi

# Assign environment variables with default values if not set
DB_USER=${POSTGRESQL_DB_USER:-postgres}
DB_PASSWORD=${POSTGRESQL_DB_PASSWORD:-admin}
DB_HOST=${POSTGRESQL_DB_HOST:-db}
DB_PORT=${POSTGRESQL_DB_PORT:-5432}
DB_NAME=${POSTGRESQL_DB_NAME}

# Path to the SQL dump file
DUMP_FILE="./var/demodata/dump.sql"

# Verify that the dump file exists
if [ ! -f "$DUMP_FILE" ]; then
    error_exit "Dump file '$DUMP_FILE' does not exist."
fi

echo "Environment Variables:"
echo "  DB_USER:     $DB_USER"
echo "  DB_PASSWORD: $DB_PASSWORD"
echo "  DB_HOST:     $DB_HOST"
echo "  DB_PORT:     $DB_PORT"
echo "  DB_NAME:     $DB_NAME"
echo "  DUMP_FILE:   $DUMP_FILE"
echo "----------------------------------------"

# Function to import the SQL dump into PostgreSQL
function import_dump {
    echo "Starting database import from '$DUMP_FILE'..."

    # Check if Docker Compose service 'db' is running
    if ! docker compose ps | grep -q "db"; then
        error_exit "Docker Compose service 'db' is not running. Please start it with 'docker compose up -d db'."
    fi

    # Import the SQL dump using psql inside the Docker container
    cat "$DUMP_FILE" | docker compose exec -T db psql -U "$DB_USER" -d "$DB_NAME" || {
        error_exit "Failed to import the database dump."
    }

    echo "Database import completed successfully."
}

# Execute the import function
import_dump

# Optional: Verify the import by listing tables (uncomment to use)
# echo "Verifying the import by listing tables..."
# docker compose exec -T db psql -U "$DB_USER" -d "$DB_NAME" -c "\dt"

# Exit the script successfully
exit 0
