#!/bin/bash

# Wait for the PostgreSQL database to be ready
echo "Waiting for the PostgreSQL database at $POSTGRESQL_DB_HOST:$POSTGRESQL_DB_PORT..."
while ! nc -z $POSTGRESQL_DB_HOST $POSTGRESQL_DB_PORT; do
  sleep 0.1
done
echo "Database is up and running!"

# Export FLASK_APP if not already set
export FLASK_APP=${FLASK_APP:-web}

# Run database migrations
echo "Running database migrations..."
flask db upgrade --directory web/migrations

# Start the Flask application
echo "Starting the Flask application..."
exec python -m web
