#!/bin/bash

# Check if POSTGRESQL_DB_HOST and POSTGRESQL_DB_PORT are set
if [[ -z "$POSTGRESQL_DB_HOST" || -z "$POSTGRESQL_DB_PORT" ]]; then
  echo "Error: POSTGRESQL_DB_HOST or POSTGRESQL_DB_PORT is not set."
  exit 1
fi


# Wait for the PostgreSQL database to be ready
echo "Waiting for the PostgreSQL database at $POSTGRESQL_DB_HOST:$POSTGRESQL_DB_PORT..."
while ! nc -z $POSTGRESQL_DB_HOST $POSTGRESQL_DB_PORT; do
  sleep 0.1
done
echo "Database is up and running!"

# Set the PYTHONPATH explicitly
export PYTHONPATH=/app

# Export FLASK_APP if not already set
export FLASK_APP=${FLASK_APP:-web}

# Run database migrations
#echo "Running database migrations..."
#flask db upgrade --directory web/migrations
# Check the PYTHONPATH
echo "PYTHONPATH is set to: $PYTHONPATH"

mkdir -p /app/var
chown -R appuser:appuser /app/var

# Start the Flask application
echo "Starting the Flask application..."
su -c "exec python -m web" appuser
