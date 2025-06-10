.PHONY: help install install-dev test coverage lint format run clean docker-build docker-up docker-down

PYTHON := python
PIP := pip
# Detect OS and set appropriate commands
ifeq ($(OS),Windows_NT)
	RM := rmdir /s /q
	RM_FILES := del /f /q
	# For Windows, use these commands to clean up
	CLEAN_CMD := if exist __pycache__ $(RM) __pycache__ & \
				if exist .pytest_cache $(RM) .pytest_cache & \
				if exist htmlcov $(RM) htmlcov & \
				if exist .coverage $(RM_FILES) .coverage & \
				if exist .coverage.* $(RM_FILES) .coverage.*
else
	RM := rm -rf
	# For Unix-based systems
	CLEAN_CMD := $(RM) __pycache__ .pytest_cache htmlcov .coverage .coverage.*
endif

help:
	@echo "Available commands:"
	@echo "  make install         Install production dependencies"
	@echo "  make install-dev     Install development dependencies"
	@echo "  make test            Run tests"
	@echo "  make coverage        Run tests with coverage"
	@echo "  make lint            Run linting"
	@echo "  make format          Run code formatting"
	@echo "  make run             Run the FastAPI server"
	@echo "  make clean           Clean up temporary files"
	@echo "  make docker-build    Build Docker images"
	@echo "  make docker-up       Start Docker containers"
	@echo "  make docker-down     Stop Docker containers"

install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -r requirements-dev.txt

test:
	$(PYTHON) -m pytest -v

coverage:
	$(PYTHON) -m pytest --cov=app --cov-report=term --cov-report=html

lint:
	$(PYTHON) -m flake8 .

format:
	$(PYTHON) -m black .
	$(PYTHON) -m isort .

run:
	$(PYTHON) -m uvicorn app.main:app --reload

clean:
	$(CLEAN_CMD)

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down
