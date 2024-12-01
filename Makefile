# Load .env
include .env.dev
export $(shell sed 's/=.*//' .env.dev)

# Define variables
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

# Install dependencies
install: $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r dev_requirements.txt

# Clean up
clean:
	rm -rf $(VENV_DIR)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

start_server:
	docker compose -f infrastructure/docker-compose.yml up

build_and_start_server:
	docker compose -f infrastructure/docker-compose.yml up --build -d

start_server_and_exec:
	docker compose -f infrastructure/docker-compose.yml up -d
	docker compose -f infrastructure/docker-compose.yml exec fastapi bash

run_tests:
	pytest tests

run_tests_with_coverage:
	coverage run -m pytest tests && coverage report -m

run_tests_in_docker:
	docker compose -f infrastructure/docker-compose.yml exec fastapi make run_tests

run_tests_with_coverage_in_docker:
	docker compose -f infrastructure/docker-compose.yml exec fastapi make run_tests_with_coverage

run_celery:
	celery -A src.taskworker.celery_app worker --loglevel=INFO

run_fastapi:
	uvicorn src.webserver.main:app --host 0.0.0.0 --port 8000 --reload --log-config src/log_config.json


.PHONY: install test run clean
.PHONY: start_server build_and_start_server start_server_and_exec
.PHONY: run_tests run_tests_with_coverage run_tests_in_docker run_tests_with_coverage_in_docker