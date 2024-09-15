# Makefile for Docker Compose

# The name of the Docker Compose file
COMPOSE_FILE=docker-compose.yml

# Target to bring up the Docker Compose services
up:
	docker compose -f $(COMPOSE_FILE) up -d

# Target to bring down the Docker Compose services
down:
	docker compose -f $(COMPOSE_FILE) down

# Optional target to show the status of Docker Compose services
status:
	docker compose -f $(COMPOSE_FILE) ps

# Optional target to view logs of Docker Compose services
logs:
	docker compose -f $(COMPOSE_FILE) logs

restart:
	docker compose -f $(COMPOSE_FILE) down && docker-compose -f $(COMPOSE_FILE) up -d


flask:
	docker compose exec loopai_web flask --app web/web_interface run --port 5000

# Target to run Flask database migration
flash_db_migrate:
	docker compose exec loopai_web . .venv/bin/activate && flask --app web/web_interface db migrate -m "ADD SOME COMMENT HERE"

# Target to run Flask database upgrade
flash_db_upgrade:
	docker compose exec loopai_web . .venv/bin/activate && flask --app web/web_interface db upgrade

# Target to access the web container console for debugging as a non-root user
bash:
	docker compose exec --user appuser web /bin/bash
