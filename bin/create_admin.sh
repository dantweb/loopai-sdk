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

# Generate a hash of the password 'Loopai_2025!'
ENCRYPTED_PASSWORD=$(docker-compose exec -T web python3 -c "import bcrypt; print(bcrypt.hashpw(b'Loopai_2025!'.encode('utf-8'), bcrypt.gensalt()).decode())")



# SQL query to check if the user exists and create the user if not
SQL_QUERY="
DO
\$do\$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM \"user\" WHERE login = 'admin') THEN
      INSERT INTO \"user\" (name, login, password, role, active)
      VALUES ('Admin User', 'admin', '$ENCRYPTED_PASSWORD', 'ADMIN', true);
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
echo "testing...."

docker-compose exec -T db psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT login, password FROM \"user\" WHERE login = 'admin';"
