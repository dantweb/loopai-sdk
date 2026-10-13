# Makefile for Docker Compose

# The name of the Docker Compose file
COMPOSE_FILE=docker-compose.yml

# Full developer install: clone core/web/view, .env, containers, DB, admin user
install:
	./bin/install.sh

# Target to bring up the Docker Compose services
#up:
#	docker compose --profile conditional -f $(COMPOSE_FILE) up --remove-orphans -d
up:
	docker compose -f $(COMPOSE_FILE) up --remove-orphans -d

upp:
	docker compose -f $(COMPOSE_FILE) down  --remove-orphans && docker compose -f $(COMPOSE_FILE) up --build --remove-orphans -d

# Target to bring down the Docker Compose services
down:
	docker compose -f $(COMPOSE_FILE) down  --remove-orphans

# Optional target to show the status of Docker Compose services
status:
	docker compose -f $(COMPOSE_FILE) ps

# Optional target to view logs of Docker Compose services
logs:
	docker compose -f $(COMPOSE_FILE) logs

restart:
	docker compose -f $(COMPOSE_FILE) down && docker compose -f $(COMPOSE_FILE) up -d


flask:
	docker compose exec loopai_web flask --app web/web_interface run --port 5000

# Target to run Flask database migration
flash_db_migrate:
	docker compose exec loopai_web flask --app web db migrate -d web/migrations -m "ADD SOME COMMENT HERE"

# Target to run Flask database upgrade
flash_db_upgrade:
	docker compose exec loopai_web flask --app web db upgrade -d web/migrations

# Target to access the web container console for debugging as a non-root user
bash:
	docker compose exec --user appuser loopai_web /bin/bash

root:
	docker compose exec --user root loopai_web /bin/bash

# Target to access the web container console for debugging as a non-root user
post:
	docker compose exec agent_post /bin/bash

bank:
	docker compose exec agent_bank /bin/bash


front:
	docker compose exec frontend bash

# Upgrade a Python package
upgrade-package:
	docker compose exec loopai_web pip install --upgrade $(PACKAGE)

# Rebuild Docker images
rebuild:
	docker compose build --no-cache loopai_web

# Run tests
run_web_tests:
	docker compose run --rm --entrypoint "" \
	  -e OPENBLAS_VERBOSE=0 \
	  loopai_web \
	  python -W ignore::DeprecationWarning -m unittest discover -s web/tests -p "test*.py" -v

run_core_tests:
	docker compose exec -w /app/core loopai_web python -m unittest discover tests.unit

# Apply web (alembic) and core migrations
migrate:
	docker compose exec loopai_web python3 core/migrations/migration202406042420.py
	docker compose exec loopai_web flask --app web db upgrade -d web/migrations
	docker compose exec loopai_web python3 core/migrations/migration202406042420.py

app_network:
	docker network inspect app_network >/dev/null 2>&1 || docker network create --driver bridge app_network
