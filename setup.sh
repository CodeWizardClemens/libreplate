#!/usr/bin/env bash
#
# LibrePlate installer
#
# Generate an environment file, if the user has not already made one.
#
# Run:
# DB_HOST=localhost \
# DB_NAME=libreplate_db \
# DB_USER=libreplate \
# DB_PASSWORD='secret' \
# ALLOWED_HOSTS=libreplate.example.com \
# bash setup.sh

# Enable strict Bash error handling:
# -e  Exit immediately if any command fails.
# -u  Treat unset variables as errors instead of silently using empty values.
# -o pipefail  Make a pipeline fail if any command in the pipeline fails
#              (not only the last command).
set -euo pipefail

# Restrict permissions on newly created files and directories:
# - Only the current user can read/write them by default.
# - Helps protect sensitive installer output such as logs and .env files.
# - A common default is 022, which would allow other users on the machine to
#   read files by default.
umask 077

APP_NAME="libreplate"
BASE_DIR="$(pwd)"
VENV_DIR="${BASE_DIR}/.venv"
ENV_FILE="${BASE_DIR}/.env"
LOG_FILE="${BASE_DIR}/install.log"
PYTHON_BIN="${PYTHON_BIN:-python3}"
PYTHON_REQUIRED_MAJOR=3
PYTHON_REQUIRED_MINOR=10
POSTGRES_REQUIRED_MAJOR=13

# Log all normal output to both the console and the installer log file.
exec > >(tee -a "$LOG_FILE")

# Send error output to the same destination as normal output.
exec 2>&1

log() {
    echo
    echo "==> $1"
}

fail() {
    echo
    echo "ERROR: $1"
    exit 1
}

check_python() {
    log "Checking Python"

    if ! command -v "$PYTHON_BIN" &>/dev/null; then
        fail "Python not found: $PYTHON_BIN"
    fi

    local python_major
    local python_minor

    read -r python_major python_minor < <(
        "$PYTHON_BIN" -c "import sys; print(sys.version_info.major, sys.version_info.minor)"
    )

    local python_version="${python_major}.${python_minor}"

    echo "Python version: ${python_version}"

    if (( python_major < PYTHON_REQUIRED_MAJOR )) || \
       (( python_major == PYTHON_REQUIRED_MAJOR && python_minor < PYTHON_REQUIRED_MINOR )); then
        fail "Python ${PYTHON_REQUIRED_MAJOR}.${PYTHON_REQUIRED_MINOR}+ required. Found ${python_version}"
    fi

    echo "Python version OK"
}

check_postgresql() {
    log "Checking PostgreSQL"

    if ! command -v psql >/dev/null 2>&1; then
        fail "PostgreSQL client (psql) not found"
    fi

    POSTGRES_VERSION=$(psql --version | awk '{print $3}')
    POSTGRES_MAJOR=$(echo "$POSTGRES_VERSION" | cut -d. -f1)

    echo "PostgreSQL version: ${POSTGRES_VERSION}"

    if (( POSTGRES_MAJOR < POSTGRES_REQUIRED_MAJOR )); then
        fail "PostgreSQL ${POSTGRES_REQUIRED_MAJOR}+ required"
    fi

    echo "PostgreSQL version OK"
}

create_directories() {
    log "Creating directories"

    mkdir -p \
        "${BASE_DIR}/uploads" \
        "${BASE_DIR}/static" \
        "${BASE_DIR}/logs"
    echo "Creating directories OK"

}

create_virtualenv() {
    log "Creating virtual environment"
    if [[ ! -d "$VENV_DIR" ]]; then
        "$PYTHON_BIN" -m venv "$VENV_DIR"
        echo "Virtual environment OK"

    else
        echo "Virtualenv already exists"
    fi
}

install_dependencies() {
    if [[ ! -f "${BASE_DIR}/requirements.txt" ]]; then
        fail "requirements.txt not found"
    fi

    # Example: django-htmx==1.27.0
    if ! grep -qE '^[^#].*==.*$' requirements.txt; then
        fail "requirements.txt must contain pinned versions (package==version)"
    fi

    log "Installing Python dependencies"
    source "${VENV_DIR}/bin/activate"
    python -m pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    deactivate
}

generate_secret() {
"$PYTHON_BIN" <<'PY'
import secrets
print(secrets.token_hex(32))
PY
}

create_env_file() {
    log "Creating environment file"

    if [[ -f "$ENV_FILE" ]]; then
        echo ".env already exists, keeping existing file"
        return
    fi

    SECRET_KEY="$(generate_secret)"
    {
        printf 'APP_ENV=production\n'
        printf 'DEBUG=False\n'
        printf 'SECRET_KEY=%s\n' "$SECRET_KEY"
        printf 'ALLOWED_HOSTS=%s\n' "$ALLOWED_HOSTS"
        printf 'DATABASE_URL=postgres://%s:%s@%s:5432/%s\n' \
            "$DB_USER" \
            "$DB_PASSWORD" \
            "$DB_HOST" \
            "$DB_NAME"
    } > "$ENV_FILE"

    chmod 600 "$ENV_FILE"
}


run_django_setup() {
    if [[ ! -f manage.py ]]; then
        echo "No Django project detected"
        return
    fi

    log "Running Django migrations"
    source "${VENV_DIR}/bin/activate"
    python manage.py migrate --noinput
    log "Collecting static files"
    python manage.py collectstatic --noinput
    deactivate
}

print_next_steps() {
cat <<EOF

Next steps:

  1. Environment file
     ${ENV_FILE}

  2. Activate virtual environment
     source ${VENV_DIR}/bin/activate

  3. Start application
     ${VENV_DIR}/bin/gunicorn libreplate.wsgi:application

EOF
}

check_environment_variables() {
    log "Checking environment variables"

    local missing=()
    local value

    for name in DB_HOST DB_NAME DB_USER DB_PASSWORD ALLOWED_HOSTS; do
        value="$(printenv "$name" || true)"

        if [[ -z "$value" ]]; then
            missing+=("$name")
        fi
    done

    if (( ${#missing[@]} > 0 )); then
        echo "Missing required environment variables:"
        printf '  - %s\n' "${missing[@]}"
        exit 1
    fi

    echo "Environment variables OK"
}

main() {
    log "Starting LibrePlate installer"
    check_environment_variables
    check_python
    check_postgresql
    create_directories
    create_virtualenv
    install_dependencies
    create_env_file
    run_django_setup
    log "Instalation complete!"
    print_next_steps
}

main "$@"