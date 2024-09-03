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

# Target to run the Flask web application
web_legacy:
	. .venv/bin/activate && FLASK_APP=./web/web_interface.py flask run

flask:
	flask --app web/web_interface run

# Target to run Flask database migration
flash_db_migrate:
	. .venv/bin/activate && flask --app web/web_interface db migrate -m "ADD SOME COMMENT HERE"

# Target to run Flask database upgrade
flash_db_upgrade:
	. .venv/bin/activate && flask --app web/web_interface db upgrade
