

ifdef OS
	docker_up = docker compose up -d
	docker_down = docker compose down --volumes
else
	docker_up = docker compose up -d
	docker_down = docker compose down
endif

run:
	poetry run python -m service

up:
	$(docker_up)

down:
	$(docker_down)

renew:
	poetry run alembic -c alembic.ini downgrade -1
	poetry run alembic -c alembic.ini upgrade head

test:
	poetry run pytest -vsx

async-alembic-init:
	poetry run alembic init -t async migration
	poetry run alembic -c alembic.ini revision --autogenerate -m "initial"

alembic:
	poetry run alembic -c alembic.ini upgrade head

lint:
	poetry run black service
	poetry run pylint service

isort:
	poetry run isort service

format:
	uv run ruff format service
	uv run ruff check --fix service

req:
	poetry export -f requirements.txt --without-hashes --output ./requirements.txt
