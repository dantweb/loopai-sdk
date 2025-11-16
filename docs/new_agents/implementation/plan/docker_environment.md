# Docker Environment Guide
**Created:** 2025-11-16
**For:** Living Agent Implementation

---

## Overview

LoopAI runs in a **Docker containerized environment**. Understanding the container architecture is critical for implementation, testing, and deployment.

---

## Container Architecture

### Active Containers

| Container | Purpose | Access Command | Notes |
|-----------|---------|---------------|-------|
| **loopai_web** | Flask web app, API endpoints, agent execution | `make bash` | Main application container |
| **agent_post** | Message routing, inter-agent communication | `make post` | Agent messaging system |
| **postgres** | PostgreSQL database | `docker exec -it postgres psql -U postgres` | Data persistence |
| **loopai_view** | Vue.js frontend | `make front` | Admin UI |
| **loopai_bank** | Agent bank service | `make bank` | Agent definitions |

### Container Network
- All containers communicate via Docker network
- Web API accessible at `http://loopai_web:5000` (internal) or `http://localhost:5050` (host)
- agent_post calls loopai_web API for message delivery

---

## File System Mapping

### Host vs Container Paths

**IMPORTANT:** Paths differ between host (your machine) and container (inside Docker).

#### Host Machine (macOS)
```
/Users/dantweb/dantweb/l-sdk-27a/
├── agent_post/              ← Host: agent_post code
├── loopai_src/              ← Host: main application
│   └── var/users/1/loops/   ← Host: agent configurations
└── docs/                    ← Host: documentation
```

#### Inside loopai_web Container
```
/app/
├── web/                     ← Container: web application
├── core/                    ← Container: core logic
└── var/users/1/loops/       ← Container: agent configurations (mounted volume)
```

#### Inside agent_post Container
```
/app/
├── src/                     ← Container: agent_post code
├── run_all_cycles.py        ← Container: orchestration script
└── (no loop configs here)
```

**Key Insight:** The `var/users/1/loops/` directory is a **shared volume** accessible from loopai_web container.

---

## Common Commands

### Starting/Stopping Containers

```bash
# Start all containers
make up

# Rebuild and start (use after config changes)
make upp

# Stop all containers
make down

# Check container status
make status

# View logs
make logs
```

### Accessing Containers

```bash
# Access loopai_web container (as appuser)
make bash

# Access loopai_web container (as root)
make root

# Access agent_post container
make post

# Access specific container
docker exec -it <container_name> /bin/bash
```

---

## Running Tests & Commands

### Testing Agent Actions

**From Host Machine:**
```bash
# Test agent action (API call to loopai_web)
curl http://localhost:5050/api/public/agent/8/action/GET_WORK/

# Check execution result
curl http://localhost:5050/api/public/agent/8/action/WAKEUP/
```

**Note:** Use `localhost:5050` from host, or `loopai_web:5000` from inside containers.

### Running Orchestration

**Option 1: From Host (via make)**
```bash
# Run orchestration inside agent_post container
make post
# Now inside container:
python run_all_cycles.py --days 1
```

**Option 2: Direct Docker Exec**
```bash
# Run from host without entering container
docker exec -it agent_post python run_all_cycles.py --days 1
```

**Option 3: Background Execution**
```bash
# Run in background, monitor logs
docker exec -d agent_post python run_all_cycles.py --days 5
docker logs -f agent_post
```

### Checking Agent Files

**From Host:**
```bash
# View agent tasks (host path)
ls /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/tasks/

# View current work
ls /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/current_work/
```

**From Inside loopai_web Container:**
```bash
# Enter container
make bash

# View agent tasks (container path)
ls /app/var/users/1/loops/70/filesystem/agentlife/tasks/

# View current work
ls /app/var/users/1/loops/70/filesystem/agentlife/current_work/
```

### Backing Up Agent Configurations

**From Host:**
```bash
# Backup from host file system
cd /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70
tar -czf ~/loop70_backup_$(date +%Y%m%d).tar.gz .
```

**From Inside Container:**
```bash
# Enter container
make bash

# Backup from container
cd /app/var/users/1/loops/70
tar -czf /tmp/loop70_backup_$(date +%Y%m%d).tar.gz .

# Copy backup to host
exit
docker cp loopai_web:/tmp/loop70_backup_*.tar.gz ~/
```

---

## Database Access

### PostgreSQL Commands

```bash
# Access PostgreSQL
docker exec -it postgres psql -U postgres -d loopai

# Run query
docker exec -it postgres psql -U postgres -d loopai -c "SELECT * FROM agent;"

# Check agent data
docker exec -it postgres psql -U postgres -d loopai -c "SELECT id, public_name, loop_id FROM agent;"
```

---

## Editing Files

### Where to Edit

**Configuration Files:**
- Edit on **host machine** using your IDE/editor
- Changes immediately available in containers (mounted volumes)
- Example: Edit `/Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/config/GET_WORK.yaml` on host

**Protocol Files:**
- Edit on **host machine**
- Path: `/Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/skills/project_thinking/protocols/`

**Python Code:**
- Edit on **host machine** in `/Users/dantweb/dantweb/l-sdk-27a/loopai_src/`
- May need to restart containers after changes: `make upp`

**Orchestration Scripts:**
- Edit on **host machine** in `/Users/dantweb/dantweb/l-sdk-27a/agent_post/`
- Changes available immediately in agent_post container

---

## Debugging

### View Logs

```bash
# View all container logs
make logs

# View specific container logs
docker logs loopai_web
docker logs agent_post
docker logs postgres

# Follow logs in real-time
docker logs -f agent_post

# View last 100 lines
docker logs --tail 100 loopai_web
```

### Check Container Status

```bash
# List running containers
docker ps

# Check container health
docker inspect loopai_web | grep Status

# View container resource usage
docker stats
```

### Restart Services

```bash
# Restart specific container
docker restart loopai_web

# Restart all containers
make down && make up

# Full rebuild (after code changes)
make upp
```

---

## Network & API

### API Endpoints

**From Host Machine:**
- Base URL: `http://localhost:5050`
- Example: `curl http://localhost:5050/api/public/agent/8/action/GET_WORK/`

**From Inside Containers:**
- Base URL: `http://loopai_web:5000`
- Example: `curl http://loopai_web:5000/api/public/agent/8/action/GET_WORK/`

**From agent_post Container:**
- Uses environment variable: `CITY_API_URL=http://loopai_web:5000/api/agents/cities-data/`
- Configured in agent_post `.env` file

### Port Mapping

| Container Port | Host Port | Service |
|---------------|-----------|---------|
| loopai_web:5000 | localhost:5050 | Flask API |
| postgres:5432 | localhost:5433 | PostgreSQL |
| loopai_view:8080 | localhost:8080 | Vue.js UI |

---

## Testing Workflow

### Typical Testing Sequence

1. **Prepare Test Environment (Host):**
   ```bash
   # Ensure containers running
   make status

   # If not running
   make upp
   ```

2. **Create Test Message (Host):**
   ```bash
   # Edit test message file
   nano /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/post/inbox/new/test_message.json
   ```

3. **Run Agent Action (Host):**
   ```bash
   # Test READ_POSTS
   curl http://localhost:5050/api/public/agent/8/action/READ_POSTS/
   ```

4. **Check Results (Host):**
   ```bash
   # View created tasks
   ls /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/tasks/new/

   # View task content
   cat /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/tasks/new/*.json
   ```

5. **Run Orchestration (Container):**
   ```bash
   # Enter agent_post container
   make post

   # Inside container:
   python run_all_cycles.py --days 1
   ```

6. **Monitor Execution (Host - separate terminal):**
   ```bash
   # Follow logs
   docker logs -f agent_post
   ```

7. **Verify Results (Host):**
   ```bash
   # Check completed tasks
   ls /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/tasks/done/
   ```

---

## Troubleshooting

### Common Issues

#### Container Not Running
```bash
# Check status
make status

# If stopped, start
make up

# If errors, check logs
make logs
```

#### API Not Responding
```bash
# Check loopai_web container
docker logs loopai_web

# Restart if needed
docker restart loopai_web

# Test API health
curl http://localhost:5050/api/health
```

#### File Changes Not Reflected
```bash
# For Python code changes
make upp  # Rebuild containers

# For config files (YAML, JSON)
# No restart needed, changes immediate
```

#### Database Connection Issues
```bash
# Check postgres container
docker ps | grep postgres

# Test connection
docker exec -it postgres psql -U postgres -c "SELECT 1;"

# View postgres logs
docker logs postgres
```

#### agent_post Can't Reach loopai_web
```bash
# Check network
docker network ls
docker network inspect l-sdk-27a_default

# Verify CITY_API_URL in agent_post
docker exec -it agent_post env | grep CITY_API_URL
```

---

## Environment Variables

### Key Environment Variables

**loopai_web Container:**
- `WEB_OR_CLI=web`
- `POSTGRESQL_DB_HOST=postgres`
- `OPENAI_API_KEY=...`

**agent_post Container:**
- `CITY_API_URL=http://loopai_web:5000/api/agents/cities-data/`
- `DATABASE_URL=...`

**View Environment Variables:**
```bash
# Inside container
make bash
env | grep API

# From host
docker exec loopai_web env | grep API
```

---

## Best Practices

### Development Workflow

1. **Edit files on host** (use your favorite editor)
2. **Test via API calls** from host (curl commands)
3. **Run orchestration** in agent_post container (make post)
4. **Monitor logs** from host (docker logs -f)
5. **Check results** on host file system

### Backup Before Changes

```bash
# Backup from host (recommended)
cd /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops
tar -czf ~/loop_backup_$(date +%Y%m%d_%H%M%S).tar.gz 70/
```

### Testing in Isolation

```bash
# Test single agent without full orchestration
curl http://localhost:5050/api/public/agent/8/action/GET_WORK/

# Then check execution result
curl http://localhost:5050/api/public/execution/{execution_id}/result/
```

---

## Quick Reference

### Essential Commands

```bash
# Container Management
make up          # Start containers
make down        # Stop containers
make upp         # Rebuild and start
make status      # Check status
make logs        # View logs

# Container Access
make bash        # loopai_web (appuser)
make post        # agent_post
make root        # loopai_web (root)

# Testing (from host)
curl http://localhost:5050/api/public/agent/8/action/GET_WORK/

# Orchestration (in agent_post container)
make post
python run_all_cycles.py --days 1

# Database
docker exec -it postgres psql -U postgres -d loopai

# Logs
docker logs -f agent_post
docker logs -f loopai_web
```

---

## Summary

**Key Points:**
1. ✅ All services run in Docker containers
2. ✅ Edit files on **host machine** (mounted volumes)
3. ✅ Test via **API calls** from host (curl to localhost:5050)
4. ✅ Run **orchestration** inside agent_post container (make post)
5. ✅ Monitor with **docker logs** from host
6. ✅ Use `localhost:5050` from host, `loopai_web:5000` from containers

**Remember:**
- Host paths: `/Users/dantweb/dantweb/l-sdk-27a/...`
- Container paths: `/app/...`
- Shared volume: `var/users/1/loops/` accessible from both

---

**Last Updated:** 2025-11-16
**Maintained By:** Implementation Team
**Questions?** Check docker-compose.yml or Makefile for container configuration
