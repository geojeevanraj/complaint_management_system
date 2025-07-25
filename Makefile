.PHONY: help install test lint format security clean setup-dev

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt

setup-dev: install  ## Setup development environment
	@echo "Setting up development environment..."
	@echo "Installing pre-commit hooks..."
	@echo "Development environment ready!"

test:  ## Run tests
	python -m pytest tests/ -v

test-cov:  ## Run tests with coverage
	python -m pytest tests/ -v --cov=. --cov-report=html --cov-report=xml

lint:  ## Run linting
	flake8 .
	bandit -r . --severity-level medium

format:  ## Format code
	black .
	isort .

format-check:  ## Check code formatting
	black --check .
	isort --check-only .

security:  ## Run security checks
	bandit -r . --severity-level medium
	safety check

type-check:  ## Run type checking
	mypy . --ignore-missing-imports

all-checks: format-check lint security type-check test  ## Run all checks

clean:  ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

run:  ## Run the application
	python app.py

db-setup:  ## Setup database
	python setup_database.py

demo-data:  ## Create demo data
	python create_demo_data.py
