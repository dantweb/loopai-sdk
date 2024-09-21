#!/bin/bash

# Load environment variables from the .env file
set -o allexport
source ../.env
set +o allexport

# Check if the required environment variables are set
if [ -z "$POSTGRESQL_DB_NAME" ]; then
  echo "POSTGRESQL_DB_NAME is not set in the .env file."
  exit 1
fi

# Check if PostgreSQL host, user, and password are set, otherwise use default values
DB_USER=${POSTGRESQL_DB_USER:-postgres}
DB_PASSWORD=${POSTGRESQL_DB_PASSWORD:-admin}
DB_HOST=${POSTGRESQL_DB_HOST:-db}
DB_PORT=${POSTGRESQL_DB_PORT:-5432}
DB_NAME=${POSTGRESQL_DB_NAME}

# Encrypt the password using PostgreSQL's built-in `crypt` function
ENCRYPTED_PASSWORD=$(echo -n 'loopai' | openssl passwd -6 -stdin)

# SQL query to check if the user exists and create the user if not
SQL_QUERY="
DO
\$do\$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM \"user\" WHERE login = 'admin') THEN
      INSERT INTO \"user\" (name, login, password, role, active)
      VALUES ('Admin User', 'admin', '$ENCRYPTED_PASSWORD', 'ADMIN', 1);
   END IF;
END
\$do\$;
"

# Run the SQL command using psql
echo "Creating admin user if not already exists..."

docker compose exec -T db psql -U "$DB_USER" -d "$DB_NAME" -c "$SQL_QUERY" || {
  echo "Failed to create admin user."
  exit 1
}

echo "Admin user setup completed."
