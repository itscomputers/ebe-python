default:
  just --list

ipy:
  poetry run python

test path="":
  poetry run pytest {{path}}

coverage:
  poetry run coverage

type_check:
  poetry run mypy .

lint:
  poetry run black . --check
  poetry run flake8

lint_fix:
  poetry run black .

pre_commit: lint type_check

