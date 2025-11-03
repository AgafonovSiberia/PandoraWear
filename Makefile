build:
	docker compose -f docker-compose.yaml up -d --build

build-debug:
	docker compose -f docker-compose.yaml -f docker-compose.debug.yaml up -d --build


down-debug:
	docker compose -f docker-compose.yaml -f docker-compose.debug.yaml down

down:
	docker compose -f docker-compose.yaml down

log-debug:
	docker compose -f docker-compose.yaml -f docker-compose.debug.yaml logs -f

.PHONY: migration-create
migration-create:
	docker-compose run --rm migrations uv run alembic -c alembic.ini revision --autogenerate -m "$(msg)"

.PHONY: migration-upgrade
migration-upgrade:
	docker-compose run --rm migrations uv run alembic -c alembic.ini upgrade head

migration-downgrade:
	docker-compose run --rm migrations uv run alembic -c alembic.ini downgrade -1

alembic-revision:
	alembic -c alembic.ini revision --autogenerate -m "init schema"