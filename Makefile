# Makefile for Incident Management System

.PHONY: help install install-dev run test clean lint format init-db

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements.txt -r requirements-dev.txt

run:  ## Run the development server
	python run.py

test:  ## Run tests
	pytest

clean:  ## Clean up cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

lint:  ## Run linting
	flake8 --max-line-length=88 --exclude=.venv,migrations .
	mypy --ignore-missing-imports .

format:  ## Format code
	black .
	isort .

init-db:  ## Initialize database
	python init_db.py

migrate:  ## Run database migrations
	flask db upgrade

create-migration:  ## Create a new migration
	flask db migrate -m "$(message)"

prod-server:  ## Run production server with Gunicorn
	gunicorn -w 4 -b 0.0.0.0:8000 app:app

docker-build:  ## Build Docker image
	docker build -t incident-management-system .

docker-run:  ## Run Docker container
	docker run -p 5000:5000 incident-management-system
