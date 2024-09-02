#!/bin/bash

# Función para crear el entorno virtual sin activarlo
function create_venv() {
    if ! command -v virtualenv &> /dev/null
    then
        echo "virtualenv no está instalado. Instalando virtualenv..."
        pip install virtualenv
    fi
    
    if [ ! -d "venv" ]; then
        echo "Creando entorno virtual..."
        virtualenv venv
    else
        echo "El entorno virtual ya existe."
    fi
}

# Función para instalar dependencias en el entorno virtual activado
function install_deps() {
    activate_venv
    if [ -f "requirements.txt" ]; then
        echo "Instalando dependencias..."
        pip install -r requirements.txt
    else
        echo "No se encontró el archivo requirements.txt."
        exit 1
    fi
}

function build() {
    docker-compose build
}

function up() {
    docker-compose up -d
}

function down() {
    docker-compose down
}

function migrate() {
    docker-compose exec web alembic upgrade head
}

function create_migration() {
    if [ -z "$1" ]; then
        echo "Debes proporcionar un mensaje para la migración."
        exit 1
    fi
    docker-compose exec web alembic revision --autogenerate -m "$1"
}

function test() {
    docker-compose exec web pytest
}

function local_migrate() {
    alembic upgrade head
}

function local_test() {
    pytest
}

function activate_venv() {
    if [ -d "venv" ]; then
        echo "Activando entorno virtual..."
        source venv/bin/activate
    else
        echo "El entorno virtual no existe. Ejecuta './script.sh create_venv' primero."
        exit 1
    fi
}

# Función para ejecutar la aplicación localmente
function run_local() {
    activate_venv
    echo "Ejecutando la aplicación localmente..."
    uvicorn app.main:app --reload
}

# Función para abrir Swagger en el navegador
function open_swagger() {
    echo "Abriendo Swagger en el navegador..."
    if command -v xdg-open &> /dev/null
    then
        xdg-open http://127.0.0.1:5000/swagger/
    elif command -v open &> /dev/null
    then
        open http://127.0.0.1:5000/swagger/
    else
        echo "No se pudo abrir el navegador. Por favor, abre manualmente: http://127.0.0.1:5000/swagger/"
    fi
}

case "$1" in
    build)
        build
        ;;
    up)
        up
        ;;
    down)
        down
        ;;
    migrate)
        migrate
        ;;
    create_migration)
        create_migration "$2"
        ;;
    test)
        test
        ;;
    local_migrate)
        local_migrate
        ;;
    local_test)
        local_test
        ;;
    create_venv)
        create_venv
        ;;
    install_deps)
        install_deps
        ;;
    activate_venv)
        activate_venv
        ;;
    run_local)
        run_local
        ;;
    open_swagger)
        open_swagger
        ;;
    *)
        echo "Usage: $0 {create_venv|activate_venv|install_deps|build|up|down|migrate|create_migration 'message'|test|local_migrate|local_test|run_local|open_swagger}"
        ;;
esac
