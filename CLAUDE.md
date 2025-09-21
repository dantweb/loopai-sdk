# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## LoopAI Application Overview

LoopAI is an agent-based automation system that executes predefined workflows called "loops" defined in YAML configuration files. The system processes content creation, web scraping, AI model interactions, and publishing workflows through a Flask-based web interface and a command-line execution engine.

## Development Commands

### Docker Environment
- `make up` - Start Docker containers
- `make upp` - Rebuild and start containers (recommended for development)
- `make down` - Stop Docker containers
- `make status` - Check container status
- `make logs` - View container logs

### Container Access
- `make bash` - Access main web container (loopai_web) as appuser
- `make root` - Access main web container as root
- `make post` - Access agent_post container
- `make bank` - Access agent_bank container
- `make front` - Access frontend container

### Flask Development
- `make flask` - Run Flask development server inside container
- `make flash_db_migrate` - Create new database migration
- `make flash_db_upgrade` - Apply database migrations

### Testing
- `make run_web_tests` - Run web application unit tests
- Tests located in `loopai_src/web/tests/` and `loopai_src/core/tests/`

### Installation
```bash
./bin/install.sh --web-branch production --view-branch production --core-branch production
make upp
```

Inside web container for first-time setup:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade -d web/migrations
```

## Architecture

### Core Components

**Main Application Structure:**
- `loopai_src/` - Primary application code
  - `core/` - Core loop execution engine and business logic
  - `web/` - Flask web interface and API endpoints
  - `view/` - Vue.js frontend (admin interface)
  - `var/` - Runtime data, user files, and loop execution artifacts

**Core Modules:**
- `core/controllers/loop_controller.py` - Main loop execution orchestrator
- `core/looper/looper.py` - YAML loop parser and step processor
- `core/adapters/` - External service integrations (OpenAI, WordPress, etc.)
- `core/services/` - Logging, session management, and shared utilities
- `core/models/` - Data models for steps, actions, inputs, and outputs

**Web Interface:**
- `web/web_interface.py` - Main Flask application
- `web/routes/` - API endpoint handlers
- `web/admin_models/` - SQLAlchemy database models
- `web/migrations/` - Alembic database migration scripts

### Loop Execution System

Loops are defined in YAML files with this structure:
```yaml
session:
  name: loop_name
  code_source: path/to/custom/code
  loop:
    step_name:
      description: "Step description"
      type: gpt|bash|webhook|csv
      input:
        type: csv|text|http|image
        source: path/or/url
      output:
        - text: {name: output_file}
        - csv: {name: output_file}
      action:
        executor: gpt|bash|custom
        model: gpt-3.5-turbo|gpt-4
        prompt: "AI instruction"
```

**Execution Flow:**
1. `LoopController` reads YAML configuration
2. `Looper` parses steps and creates `StepModel` instances
3. Each step executes via adapters (GPT, WordPress, etc.)
4. Results stored in `var/users/{user_id}/loops/{loop_id}/`

### Database Models

**Core Entities:**
- `User` - User accounts and authentication
- `Project` - Project containers for organizing loops
- `Loop` - Individual loop definitions and metadata
- `Agent`, `AgentRole`, `AgentStatus` - Agent-based interaction system
- `Action` - Available agent actions (WAKEUP, MSG, etc.)

### Key Services

**Session Management:**
- User, project, and loop context tracking
- Session isolation for concurrent executions

**Broadcasting:**
- Real-time updates via Socket.IO
- Progress notifications during loop execution

**File System:**
- User-isolated directory structure at `var/users/{user_id}/`
- Loop artifacts stored per execution

## Running Loops

### Command Line (Single User)
```bash
python3 loopai_src/app.py /abs/path/to/loop_config.yaml --user 1 --loopId 17
```

### Web-based Execution
```bash
python3 web/command/cron_runner.py --loopId 17 --user 1
```

### Production Cron
```bash
docker compose exec -T -e RUNNING_CRON=True web python3 web/command/cron_runner.py --loopId 17 --user 1
```

## Database Management

### PostgreSQL Backup
```bash
python database_backup.py --env_file=.env
```

### Recreate Loops Table
```bash
python web/command/populate_loops_script.py --user_id=1 --project_id=1 --base_directory=/app/var/users/1/loops
```

## Frontend Development

Vue.js admin interface:
```bash
cd loopai_src/view/vue/admin
npm install
npm run serve
```

## Environment Configuration

Key environment variables in `.env`:
- `WEB_OR_CLI=cli|web` - Execution mode
- `POSTGRESQL_DB_*` - Database connection settings
- `OPENAI_API_KEY` - AI model access
- `VUE_APP_API_BASE_*` - Frontend API configuration

## Common Development Patterns

### Adding New Loop Step Types
1. Create adapter in `core/adapters/`
2. Register executor in step processing logic
3. Add corresponding models if needed

### Database Schema Changes
1. Modify models in `web/admin_models/`
2. Generate migration: `make flash_db_migrate`
3. Apply changes: `make flash_db_upgrade`

### Custom Loop Actions
- Place custom Python code in loop's `code_source` directory
- Reference in YAML via `executor: custom`
- Code automatically imported during execution