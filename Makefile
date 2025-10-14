PYTHON ?= python3
VENV_DIR ?= .venv
ACTIVATE := . $(VENV_DIR)/bin/activate

.PHONY: venv install run test clean docker-build docker-up docker-down

venv:
$(PYTHON) -m venv $(VENV_DIR)

install: venv
$(ACTIVATE) && pip install --upgrade pip
$(ACTIVATE) && pip install -r requirements.txt

run:
$(ACTIVATE) && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test:
$(ACTIVATE) && pytest

clean:
rm -rf $(VENV_DIR)
rm -rf __pycache__ */__pycache__

# Utilidades adicionales

docker-build:
docker build -t order-processing-service .

docker-up:
docker-compose up --build

docker-down:
docker-compose down
