#!/bin/bash

# Exit on any error
set -e


echo "Stopping running Docker containers..."
docker compose down || { echo "Failed to stop Docker containers"; exit 1; }

echo "Rebuilding and starting Docker containers..."
docker compose up -d --build || { echo "Failed to build and start Docker containers"; exit 1; }


create_db.sh

# Run Alembic migrations
echo "Running Alembic migrations..."
# Execute Alembic migration commands inside the appropriate Docker container (assumed to be 'web')
docker compose exec loopai_web alembic -c /app/web/migrations/alembic.ini upgrade head || { echo "Failed to run Alembic migrations"; exit 1; }

# Install any missing Python packages
echo "Installing missing Python packages..."
docker compose exec web /app/bin/install_missing_py_pkg.sh || { echo "Failed to install missing Python packages"; exit 1; }

# Clean up old Docker images to free up space
echo "Cleaning up old Docker images..."
docker image prune -f || { echo "Failed to clean up Docker images"; exit 1; }

echo "Deployment completed successfully."
