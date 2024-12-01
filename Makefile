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
	$(PIP) install -r requirements.txt

# Run tests
test: $(VENV_DIR)
	$(PYTHON) -m unittest discover -s tests

# Run the application
run: $(VENV_DIR)
	$(PYTHON) manage.py runserver 0.0.0.0:8000

# Clean up
clean:
	rm -rf $(VENV_DIR)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

start_server:
	docker compose -f infrastructure/docker-compose.yml up

start_server_with_build:
	docker compose -f infrastructure/docker-compose.yml up --build


.PHONY: install test run clean start_server