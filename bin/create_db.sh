#!/bin/bash

# Load environment variables from the .env file
set -o allexport
source .env
set +o allexport

# Check if POSTGRESQL_DB_NAME is set
if [ -z "$POSTGRESQL_DB_NAME" ]; then
  echo "POSTGRESQL_DB_NAME is not set in the .env file."
  exit 1
fi

# Check if POSTGRESQL_DB_NAME_WEB is set
if [ -z "$POSTGRESQL_DB_NAME_WEB" ]; then
  echo "POSTGRESQL_DB_NAME_WEB is not set in the .env file."
  exit 1
fi

# Check if POSTGRESQL_DB_USER is set, otherwise default to 'postgres'
DB_USER=${POSTGRESQL_DB_USER:-postgres}

# Check if POSTGRESQL_DB_PASSWORD is set, otherwise default to 'admin'
DB_PASSWORD=${POSTGRESQL_DB_PASSWORD:-admin}

# Check if POSTGRESQL_DB_HOST is set, otherwise default to 'db'
DB_HOST=${POSTGRESQL_DB_HOST:-db}

# Check if POSTGRESQL_DB_PORT is set, otherwise default to '5432'
DB_PORT=${POSTGRESQL_DB_PORT:-5432}

echo "Creating database '$POSTGRESQL_DB_NAME' if it does not exist..."

# Create POSTGRESQL_DB_NAME if it does not exist
docker compose exec -T db psql -U "$DB_USER" -d postgres -c "SELECT 1 FROM pg_database WHERE datname = '$POSTGRESQL_DB_NAME'" | grep -q 1 || \
docker compose exec -T db psql -U "$DB_USER" -d postgres -c "CREATE DATABASE \"$POSTGRESQL_DB_NAME\";" || {
  echo "Failed to create the database '$POSTGRESQL_DB_NAME'."
  exit 1
}

echo "Creating database '$POSTGRESQL_DB_NAME_WEB' if it does not exist..."

# Create POSTGRESQL_DB_NAME_WEB if it does not exist
docker compose exec -T db psql -U "$DB_USER" -d postgres -c "SELECT 1 FROM pg_database WHERE datname = '$POSTGRESQL_DB_NAME_WEB'" | grep -q 1 || \
docker compose exec -T db psql -U "$DB_USER" -d postgres -c "CREATE DATABASE \"$POSTGRESQL_DB_NAME_WEB\";" || {
  echo "Failed to create the database '$POSTGRESQL_DB_NAME_WEB'."
  exit 1
}

echo "Databases '$POSTGRESQL_DB_NAME' and '$POSTGRESQL_DB_NAME_WEB' are ready."

cd ..
