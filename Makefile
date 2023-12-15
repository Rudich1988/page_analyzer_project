install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b localhost:$(PORT) page_analyzer:app

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

lint:
	poetry run flake8 page_analyzer

selfcheck:
	poetry check

check: selfcheck test lint

build:
	./build.sh

.PHONY: install test lint check build