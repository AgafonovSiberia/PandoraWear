build:
	docker compose -f docker-compose.yaml up -d --build $(app)

log:
	docker compose -f docker-compose.yaml logs -f $(app)

down:
	docker compose -f docker-compose.yaml down $(app)


build-debug:
	docker compose --env-file ./debug.env -f docker-compose.yaml -f docker-compose.debug.yaml up -d --build $(app)


down-debug:
	docker compose -f docker-compose.yaml -f docker-compose.debug.yaml down $(app)


log-debug:
	docker compose -f docker-compose.yaml -f docker-compose.debug.yaml logs -f $(app)

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