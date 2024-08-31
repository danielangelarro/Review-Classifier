#!/bin/bash

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
    *)
        echo "Usage: $0 {build|up|down|migrate|create_migration 'message'|test|local_migrate|local_test}"
        ;;
esac