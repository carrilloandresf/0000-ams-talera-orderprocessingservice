SHELL := /bin/bash

PYTHON ?= /opt/homebrew/bin/python3.11
VENV_DIR ?= .venv

PIP := $(VENV_DIR)/bin/pip
PY := $(VENV_DIR)/bin/python
UVICORN := $(VENV_DIR)/bin/uvicorn

.PHONY: venv install run test clean docker-build docker-up docker-down

venv:
	$(PYTHON) -m venv $(VENV_DIR)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(UVICORN) src.main:app --reload --host 0.0.0.0 --port 8000

test:
	$(VENV_DIR)/bin/pytest -q

clean:
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Utilidades adicionales

docker-build:
	docker build -t order-processing-service .

# En Docker Desktop moderno es "docker compose", no "docker-compose"
docker-up:
	docker compose up --build

docker-down:
	docker compose down