#!/bin/bash

# Determine the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

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

# Check if the required environment variables are set
if [ -z "$POSTGRESQL_DB_NAME_WEB" ]; then
  echo "POSTGRESQL_DB_NAME_WEB is not set in the .env file."
  exit 1
fi

# Check if PostgreSQL host, user, and password are set, otherwise use default values
DB_USER=${POSTGRESQL_DB_USER:-postgres}
DB_PASSWORD=${POSTGRESQL_DB_PASSWORD:-admin}
DB_HOST=${POSTGRESQL_DB_HOST:-db}
DB_PORT=${POSTGRESQL_DB_PORT:-5432}
DB_NAME=${POSTGRESQL_DB_NAME_WEB}

echo "Using database: $DB_NAME"
echo "Generating password hash..."

# Generate a hash of the password 'Loopai_2025!'
# Fixed the Python command to properly handle bytes
ENCRYPTED_PASSWORD=$(docker compose exec -T loopai_web python3 -c "import bcrypt; print(bcrypt.hashpw('Loopai_2025!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))")

if [ -z "$ENCRYPTED_PASSWORD" ]; then
    echo "Failed to generate password hash. Is the loopai_web container running?"
    exit 1
fi

echo "Password hash generated successfully."

# SQL query to check if the user exists and create the user if not
SQL_QUERY="
DO
\$do\$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM \"user\" WHERE login = 'admin2') THEN
      INSERT INTO \"user\" (name, login, password, role, active)
      VALUES ('Admin User', 'admin2', '$ENCRYPTED_PASSWORD', 'ADMIN', true);
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
echo "Verifying admin user was created:"

docker compose exec -T db psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT login, role FROM \"user\" WHERE login = 'admin';"