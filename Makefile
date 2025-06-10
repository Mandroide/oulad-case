install:       ## Install project with Poetry
	poetry install

lint:          ## black + ruff + mypy
	poetry run ruff check src tests
	poetry run black --check src tests
	poetry run mypy src tests

test:          ## Pytest with coverage
	poetry run pytest -q

run:           ## Execute full ETL
	poetry run oulad-etl run
