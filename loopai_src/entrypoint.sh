#!/bin/bash -e

# Determine if we're running inside Docker by checking /proc/1/cgroup
if grep -q docker /proc/1/cgroup; then
  echo "Detected running inside Docker."
  # Inside Docker: Use the service name for PostgreSQL
  POSTGRESQL_DB_HOST=${POSTGRESQL_DB_HOST:-postgres}
else
  echo "Detected running on the host."
  # On the host: Use localhost or a configured PostgreSQL host
  POSTGRESQL_DB_HOST=${POSTGRESQL_DB_HOST:-localhost}
fi

# Check if POSTGRESQL_DB_PORT is set
if [[ -z "$POSTGRESQL_DB_PORT" ]]; then
  echo "Error: POSTGRESQL_DB_PORT is not set. Setting it to default 5432."
  export POSTGRESQL_DB_PORT=5432

fi

# Wait for the PostgreSQL database to be ready
echo "Waiting for the PostgreSQL database at $POSTGRESQL_DB_HOST:$POSTGRESQL_DB_PORT..."
timeout 60 bash -c "until nc -z $POSTGRESQL_DB_HOST $POSTGRESQL_DB_PORT; do sleep 0.1; done" || {
  echo "Error: PostgreSQL database not reachable after 60 seconds."
  exit 1
}
echo "Database is up and running!"

# Set the PYTHONPATH explicitly
export PYTHONPATH=/app

# Export FLASK_APP if not already set
export FLASK_APP=${FLASK_APP:-web}

# Run database migrations (optional, uncomment if needed)
# echo "Running database migrations..."
# flask db upgrade --directory web/migrations

# Check the PYTHONPATH
echo "PYTHONPATH is set to: $PYTHONPATH"

# Start the Flask application
echo "Starting the Flask application..."
exec python -m web
