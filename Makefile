install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run

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

build: check
		poetry build

.PHONY: install test lint check build