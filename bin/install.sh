#!/usr/bin/env bash
#
# LoopAI developer installer.
#
# Clones/updates the three source repositories into ./loopai_src
# (core, web, view), prepares .env files, builds and starts the Docker
# stack, initialises the database (migrations, defaults, admin user) and
# smoke-tests core, CLI, web and frontend.
#
# Safe to re-run: existing checkouts are updated (never wiped unless
# --fresh is given) and existing .env files are never overwritten.
#
# Usage: ./bin/install.sh [options]   (run --help for the list)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# ---------------------------------------------------------------------------
# Defaults / options
# ---------------------------------------------------------------------------
DEFAULT_BRANCH="production"
WEB_BRANCH="$DEFAULT_BRANCH"
VIEW_BRANCH="$DEFAULT_BRANCH"
CORE_BRANCH="$DEFAULT_BRANCH"
USE_HTTP=false
FRESH=false
SKIP_DOCKER=false
SKIP_FRONTEND=false
ADMIN_LOGIN="admin"
ADMIN_PASSWORD="Loopai_2025!"
ADMIN_EMAIL="admin@loopai.local"

usage() {
    cat <<EOF
Usage: ./bin/install.sh [options]

Branch parameters:
  --web-branch <branch>    Branch for dantweb/loopai-web   (default: $DEFAULT_BRANCH)
  --view-branch <branch>   Branch for dantweb/loopai-view  (default: $DEFAULT_BRANCH)
  --core-branch <branch>   Branch for dantweb/loopai-core  (default: $DEFAULT_BRANCH)
  --all-same <branch>      Use the same branch for all repositories

Other options:
  --force-http             Clone over HTTPS instead of SSH (CI / no SSH key)
  --fresh                  Wipe and re-clone existing checkouts (web/users is kept)
  --no-docker              Only clone repositories and prepare .env files
  --no-frontend            Do not build/start the Vue admin (frontend) container
  --admin-login <login>    Admin user to create   (default: $ADMIN_LOGIN)
  --admin-password <pass>  Admin user password    (default: $ADMIN_PASSWORD)
  -h, --help               Show this help

Host ports can be overridden in ./.env: LOOPAI_WEB_PORT (5050),
LOOPAI_DEBUG_PORT (5678), LOOPAI_DB_PORT (5432), LOOPAI_REDIS_PORT (6379),
LOOPAI_FRONTEND_PORT (8080). Busy db/redis/frontend/debug ports are
replaced by free ones automatically (and saved to ./.env).
EOF
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --web-branch) WEB_BRANCH="$2"; shift ;;
        --view-branch) VIEW_BRANCH="$2"; shift ;;
        --core-branch) CORE_BRANCH="$2"; shift ;;
        --all-same) WEB_BRANCH="$2"; VIEW_BRANCH="$2"; CORE_BRANCH="$2"; shift ;;
        --force-http) USE_HTTP=true ;;
        --fresh) FRESH=true ;;
        --no-docker) SKIP_DOCKER=true ;;
        --no-frontend) SKIP_FRONTEND=true ;;
        --admin-login) ADMIN_LOGIN="$2"; shift ;;
        --admin-password) ADMIN_PASSWORD="$2"; shift ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Unknown parameter passed: $1"; usage; exit 1 ;;
    esac
    shift
done

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
step() { echo; echo "==> $*"; }
info() { echo "    $*"; }
warn() { echo "    WARNING: $*" >&2; }
die()  { echo "ERROR: $*" >&2; exit 1; }

get_repo_url() {
    local repo=$1
    if [ "$USE_HTTP" = true ]; then
        echo "https://github.com/${repo}.git"
    else
        echo "git@github.com:${repo}.git"
    fi
}

# Clone a repository into $dir, or update an existing checkout.
# $preserve_subdir (optional) survives --fresh re-clones (e.g. web/users).
sync_repo() {
    local dir=$1 repo_url=$2 branch=$3 preserve_subdir=${4:-}

    if [ -d "$dir/.git" ] && [ "$FRESH" = false ]; then
        info "$dir exists - updating to '$branch'"
        if [ -n "$(git -C "$dir" status --porcelain --untracked-files=no)" ]; then
            warn "$dir has uncommitted changes - leaving it on '$(git -C "$dir" branch --show-current)' untouched."
            return 0
        fi
        git -C "$dir" fetch origin "$branch" || die "Failed to fetch '$branch' in $dir"
        if git -C "$dir" show-ref --verify --quiet "refs/heads/$branch"; then
            git -C "$dir" checkout -q "$branch"
        else
            git -C "$dir" checkout -q -b "$branch" --track "origin/$branch"
        fi
        git -C "$dir" merge -q --ff-only "origin/$branch" \
            || warn "$dir: '$branch' has diverged from origin - not updated."
        return 0
    fi

    # Fresh clone. Keep the old directory (if any) as a backup until the clone succeeds.
    local backup=""
    if [ -e "$dir" ] && [ -n "$(ls -A "$dir" 2>/dev/null)" ]; then
        backup="${dir}.bak.$(date +%Y%m%d%H%M%S)"
        info "Moving existing $dir to $backup"
        mv "$dir" "$backup"
    else
        rm -rf "$dir"
    fi

    info "Cloning $repo_url (branch: $branch) into $dir"
    if ! git clone -q -b "$branch" "$repo_url" "$dir"; then
        [ -n "$backup" ] && mv "$backup" "$dir"
        die "Failed to clone $repo_url on branch $branch"
    fi

    if [ -n "$backup" ]; then
        if [ -n "$preserve_subdir" ] && [ -d "$backup/$preserve_subdir" ]; then
            info "Restoring $dir/$preserve_subdir"
            rm -rf "${dir:?}/$preserve_subdir"
            mv "$backup/$preserve_subdir" "$dir/$preserve_subdir"
        fi
        rm -rf "$backup"
    fi
}

# Create $target from $dist if missing; otherwise append keys that exist in
# $dist but not in $target (existing values are never changed).
ensure_env_file() {
    local dist=$1 target=$2
    [ -f "$dist" ] || { warn "$dist not found - skipping $target"; return 0; }
    if [ ! -f "$target" ]; then
        cp "$dist" "$target"
        info "Created $target"
        return 0
    fi
    local added=0 key line
    while IFS= read -r line || [ -n "$line" ]; do
        [[ "$line" =~ ^[[:space:]]*([A-Za-z_][A-Za-z0-9_]*)= ]] || continue
        key="${BASH_REMATCH[1]}"
        if ! grep -qE "^[[:space:]]*${key}=" "$target"; then
            [ "$added" -eq 0 ] && printf '\n# added by bin/install.sh from %s\n' "$(basename "$dist")" >> "$target"
            echo "$line" >> "$target"
            added=$((added + 1))
        fi
    done < "$dist"
    if [ "$added" -gt 0 ]; then
        info "$target exists - appended $added missing key(s) from $(basename "$dist")"
    else
        info "$target exists - kept as is"
    fi
}

env_get() {  # env_get <file> <key>  -> last value of key (unquoted), or empty
    grep -E "^[[:space:]]*$2=" "$1" 2>/dev/null | tail -1 | cut -d= -f2- | sed -e 's/^"//' -e 's/"$//' || true
}

env_set() {  # env_set <file> <key> <value>  (replace or append)
    if grep -qE "^[[:space:]]*$2=" "$1"; then
        local tmp; tmp="$(mktemp)"
        awk -v k="$2" -v v="$3" 'BEGIN{FS=OFS="="} $1==k {print k "=" v; next} {print}' "$1" > "$tmp"
        cat "$tmp" > "$1" && rm -f "$tmp"
    else
        echo "$2=$3" >> "$1"
    fi
}

port_in_use() { (exec 3<>"/dev/tcp/127.0.0.1/$1") 2>/dev/null; }

# Pick host ports for the stack. Only called when the stack is not running,
# because a running LoopAI stack occupies its own ports.
resolve_ports() {
    local spec var default port candidate
    for spec in LOOPAI_WEB_PORT:5050 LOOPAI_DEBUG_PORT:5678 LOOPAI_DB_PORT:5432 \
                LOOPAI_REDIS_PORT:6379 LOOPAI_FRONTEND_PORT:8080; do
        var="${spec%%:*}"; default="${spec##*:}"
        [ "$var" = LOOPAI_FRONTEND_PORT ] && [ "$SKIP_FRONTEND" = true ] && continue
        port="$(env_get .env "$var")"
        [ -n "$port" ] || port="$default"
        if port_in_use "$port"; then
            if [ "$var" = LOOPAI_WEB_PORT ]; then
                die "Port $port (LOOPAI_WEB_PORT) is in use. Free it, or set LOOPAI_WEB_PORT and VUE_APP_API_BASE_URL/VUE_APP_API_BASE_HOST in ./.env"
            fi
            candidate=$((port + 1))
            while port_in_use "$candidate"; do candidate=$((candidate + 1)); done
            warn "Port $port for $var is in use - using $candidate (saved in ./.env)"
            port="$candidate"
            env_set .env "$var" "$port"
        fi
    done
}

compose() { docker compose "$@"; }
web_exec() { compose exec -T loopai_web "$@"; }

# ---------------------------------------------------------------------------
# 1. Prerequisites
# ---------------------------------------------------------------------------
step "Checking prerequisites"
command -v git >/dev/null || die "git is not installed"
if [ "$SKIP_DOCKER" = false ]; then
    command -v docker >/dev/null || die "docker is not installed"
    command -v curl >/dev/null || die "curl is not installed"
    docker compose version >/dev/null 2>&1 || die "'docker compose' (v2 plugin) is not available"
    docker info >/dev/null 2>&1 || die "Docker daemon is not running"
fi
info "OK"

# ---------------------------------------------------------------------------
# 2. Source repositories
# ---------------------------------------------------------------------------
step "Syncing source repositories (core: $CORE_BRANCH, web: $WEB_BRANCH, view: $VIEW_BRANCH)"
sync_repo "./loopai_src/core" "$(get_repo_url dantweb/loopai-core)" "$CORE_BRANCH"
sync_repo "./loopai_src/web"  "$(get_repo_url dantweb/loopai-web)"  "$WEB_BRANCH" "users"
sync_repo "./loopai_src/view" "$(get_repo_url dantweb/loopai-view)" "$VIEW_BRANCH"

# ---------------------------------------------------------------------------
# 3. Environment files and runtime directories
# ---------------------------------------------------------------------------
step "Preparing .env files"
ensure_env_file .env.dist .env
ensure_env_file loopai_src/.env.dist loopai_src/.env
ensure_env_file loopai_src/view/vue/admin/.env.dist loopai_src/view/vue/admin/.env

# On Linux the container needs the host docker.sock group to run docker steps.
if [ -S /var/run/docker.sock ] && [ "$(uname -s)" = "Linux" ] && [ -z "$(env_get .env DOCKER_SOCKET_GID)" ]; then
    env_set .env DOCKER_SOCKET_GID "$(stat -c %g /var/run/docker.sock)"
    info "Set DOCKER_SOCKET_GID=$(env_get .env DOCKER_SOCKET_GID) in ./.env"
fi

mkdir -p loopai_src/var/filesystem loopai_src/var/users loopai_src/var/logs loopai_src/var/tmp loopai_src/web/users

if [ "$SKIP_DOCKER" = true ]; then
    step "Repositories and .env files are ready (--no-docker: skipping containers and database)"
    exit 0
fi

# compose reads the same ./.env file
DB_USER="$(env_get .env POSTGRESQL_DB_USER)";         DB_USER="${DB_USER:-postgres}"
DB_NAME="$(env_get .env POSTGRESQL_DB_NAME)";         DB_NAME="${DB_NAME:-loopai}"
DB_NAME_WEB="$(env_get .env POSTGRESQL_DB_NAME_WEB)"; DB_NAME_WEB="${DB_NAME_WEB:-$DB_NAME}"

# ---------------------------------------------------------------------------
# 4. Docker stack
# ---------------------------------------------------------------------------
step "Starting Docker services"
docker network inspect shared_network >/dev/null 2>&1 || {
    info "Creating external docker network 'shared_network'"
    docker network create shared_network >/dev/null
}

if [ -z "$(compose ps -q --status running loopai_web 2>/dev/null)" ]; then
    resolve_ports
fi

SERVICES=(db redis loopai_web)
[ "$SKIP_FRONTEND" = false ] && SERVICES+=(frontend)
compose up -d --build --remove-orphans "${SERVICES[@]}" || die "Failed to build and start Docker services"

# Check over TCP: on first start the image runs initdb against a temporary
# socket-only server and then restarts, so a socket check succeeds too early.
info "Waiting for PostgreSQL..."
DB_READY=false
for _ in $(seq 1 90); do
    if compose exec -T db pg_isready -h 127.0.0.1 -U "$DB_USER" >/dev/null 2>&1; then
        DB_READY=true
        break
    fi
    sleep 1
done
[ "$DB_READY" = true ] || die "PostgreSQL did not become ready"

# ---------------------------------------------------------------------------
# 5. Database
# ---------------------------------------------------------------------------
step "Initialising database"
for name in $(printf '%s\n' "$DB_NAME" "$DB_NAME_WEB" | sort -u); do
    if compose exec -T db psql -U "$DB_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$name'" | grep -q 1; then
        info "Database '$name' exists"
    else
        compose exec -T db psql -U "$DB_USER" -d postgres -c "CREATE DATABASE \"$name\";" >/dev/null
        info "Created database '$name'"
    fi
done

# The core table (loopai_broadcast) must exist before alembic: web migration
# d46a811261f2 drops it. Core migrations are idempotent, so run them again
# afterwards to recreate it.
info "Running core migrations"
web_exec python3 core/migrations/migration202406042420.py || die "Core migrations failed"

info "Running web migrations (alembic)"
web_exec flask --app web db upgrade -d web/migrations || die "Web migrations failed"

info "Re-applying core migrations"
web_exec python3 core/migrations/migration202406042420.py || die "Core migrations failed"

psql_web() { compose exec -T db psql -U "$DB_USER" -d "$DB_NAME_WEB" -tAc "$1"; }

if [ "$(psql_web 'SELECT count(*) FROM agent_role' | tr -d '[:space:]')" = "0" ]; then
    info "Populating agent roles/statuses"
    web_exec python3 web/command/populate_defaults.py
else
    info "Agent roles/statuses already populated"
fi

info "Ensuring admin user '$ADMIN_LOGIN'"
compose exec -T -e ADMIN_LOGIN="$ADMIN_LOGIN" -e ADMIN_PASSWORD="$ADMIN_PASSWORD" -e ADMIN_EMAIL="$ADMIN_EMAIL" \
    loopai_web python3 - <<'PY' || die "Failed to create admin user"
import os
import bcrypt
from web import create_app
from web.admin_models.db import db
from web.admin_models.user import User, UserRole

login = os.environ["ADMIN_LOGIN"]
app = create_app()
with app.app_context():
    if User.query.filter_by(login=login).first():
        print(f"    Admin user '{login}' already exists")
    else:
        password = bcrypt.hashpw(os.environ["ADMIN_PASSWORD"].encode(), bcrypt.gensalt()).decode()
        db.session.add(User(name="Admin User", login=login, password=password,
                            email=os.environ["ADMIN_EMAIL"], role=UserRole.ADMIN, active=True))
        db.session.commit()
        print(f"    Created admin user '{login}'")
PY

# ---------------------------------------------------------------------------
# 6. Smoke tests
# ---------------------------------------------------------------------------
step "Verifying installation"
WEB_PORT="$(compose port loopai_web 5000 | awk -F: '{print $NF}')"
FRONTEND_PORT=""
FAILED=0

http_ok() {  # http_ok <label> <url>
    local code=000
    for _ in $(seq 1 30); do
        code="$(curl -s -o /dev/null -w '%{http_code}' "$2" || true)"
        [[ "$code" =~ ^[234] ]] && { info "$1: OK ($2 -> $code)"; return 0; }
        sleep 2
    done
    warn "$1: FAILED ($2 -> $code)"; FAILED=1
}

if web_exec python3 -c "import core.controllers.loop_controller, core.looper.looper" >/dev/null; then
    info "core: OK (imports)"
else
    warn "core: FAILED to import"; FAILED=1
fi

if web_exec python3 app.py --help >/dev/null; then
    info "cli: OK (python3 app.py --help)"
else
    warn "cli: FAILED"; FAILED=1
fi

# web: log in as the admin user (exercises web, DB, migrations and auth)
json_escape() { local s=${1//\\/\\\\}; printf '%s' "${s//\"/\\\"}"; }
LOGIN_URL="http://localhost:${WEB_PORT}/api/login/"
LOGIN_BODY="{\"username\":\"$(json_escape "$ADMIN_LOGIN")\",\"password\":\"$(json_escape "$ADMIN_PASSWORD")\"}"
LOGIN_OK=false
for _ in $(seq 1 30); do
    if curl -s -X POST -H 'Content-Type: application/json' -d "$LOGIN_BODY" "$LOGIN_URL" | grep -q '"token"'; then
        LOGIN_OK=true
        break
    fi
    sleep 2
done
if [ "$LOGIN_OK" = true ]; then
    info "web: OK (admin login via $LOGIN_URL)"
else
    warn "web: FAILED (admin login via $LOGIN_URL)"; FAILED=1
fi

if [ "$SKIP_FRONTEND" = false ]; then
    FRONTEND_PORT="$(compose port frontend 80 | awk -F: '{print $NF}')"
    http_ok "frontend" "http://localhost:${FRONTEND_PORT}/"
fi

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo
if [ "$FAILED" -ne 0 ]; then
    echo "Installation finished with errors - check 'make logs'."
    exit 1
fi
FRONTEND_URL="(skipped)"
[ -n "$FRONTEND_PORT" ] && FRONTEND_URL="http://localhost:${FRONTEND_PORT}"
cat <<EOF
LoopAI developer bundle is installed and running.

  Web API / backend : http://localhost:${WEB_PORT}
  Admin frontend    : ${FRONTEND_URL}
  Admin login       : ${ADMIN_LOGIN} / ${ADMIN_PASSWORD}

  Shell in the web container : make bash
  Run a loop from the CLI    : docker compose exec -e WEB_OR_CLI=cli loopai_web python3 app.py --loop /app/<path>/loop.yaml --user 1 --loopId <id>
  Core unit tests            : make run_core_tests
  Web unit tests             : make run_web_tests
EOF
