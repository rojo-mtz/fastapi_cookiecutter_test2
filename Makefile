# Template Microservice Makefile

.PHONY: help build up down logs shell test clean dev-up dev-down

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Production commands
build: ## Build the Docker image
	docker-compose build

up: ## Start the application in production mode
	docker-compose up -d

down: ## Stop the application
	docker-compose down

logs: ## Show application logs
	docker-compose logs -f template-microservice

# Development commands
dev-up: ## Start the application in development mode with hot reload
	docker-compose -f docker-compose.dev.yml up -d

dev-down: ## Stop the development application
	docker-compose -f docker-compose.dev.yml down

dev-logs: ## Show development logs
	docker-compose -f docker-compose.dev.yml logs -f template-microservice-dev

# Utility commands
shell: ## Access the container shell
	docker-compose exec template-microservice /bin/bash

dev-shell: ## Access the development container shell
	docker-compose -f docker-compose.dev.yml exec template-microservice-dev /bin/bash

test: ## Run tests inside the container
	docker-compose exec template-microservice python -m pytest

clean: ## Remove all containers and images
	docker-compose down --rmi all --volumes --remove-orphans
	docker-compose -f docker-compose.dev.yml down --rmi all --volumes --remove-orphans

# Local development (without Docker)
local-install: ## Install dependencies locally
	poetry install

local-run: ## Run the application locally
	poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

local-test: ## Run tests locally
	poetry run pytest
