
# Run Alembic migrations
echo "Running Alembic migrations..."
# Execute Alembic migration commands inside the appropriate Docker container (assumed to be 'web')
docker compose exec loopai_web alembic -c /app/web/migrations/alembic.ini upgrade head || { echo "Failed to run Alembic migrations"; exit 1; }

echo "Creating db tables for the LoopAI Core"
docker compose exec loopai_web python /app/core/migrations/migration202406042420.py
