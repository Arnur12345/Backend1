.PHONY: help build up down logs shell test clean migrate fix-docker

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build the Docker images
	docker-compose build --no-cache

up: ## Start the services
	docker-compose up -d

down: ## Stop the services
	docker-compose down

logs: ## Show logs
	docker-compose logs -f

logs-app: ## Show app logs
	docker-compose logs -f app

logs-db: ## Show database logs
	docker-compose logs -f db

shell: ## Access app container shell
	docker-compose exec app bash

db-shell: ## Access database shell
	docker-compose exec db psql -U user -d taskdb

restart: ## Restart services
	docker-compose restart

clean: ## Clean up containers and volumes
	docker-compose down -v
	docker system prune -f

fix-docker: ## Fix Docker issues (clean everything)
	docker-compose down -v
	docker system prune -af
	docker volume prune -f
	docker builder prune -af
	@echo "Docker cleaned! Try 'make dev' again"

reset: ## Complete reset (use if bus error persists)
	docker-compose down -v --remove-orphans
	docker system prune -af --volumes
	docker network prune -f
	docker builder prune -af
	@echo "Complete Docker reset done! Try 'make dev' again"

# Database migrations
migrate: ## Create a new migration
	docker-compose exec app alembic revision --autogenerate -m "$(msg)"

upgrade: ## Apply migrations
	docker-compose exec app alembic upgrade head

downgrade: ## Rollback last migration
	docker-compose exec app alembic downgrade -1

# Development
dev: ## Start development environment
	docker-compose up --build

dev-local: ## Start without Docker (local PostgreSQL required)
	@echo "Make sure PostgreSQL is running locally..."
	alembic upgrade head
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

install: ## Install dependencies locally
	pip install -r requirements.txt

test: ## Run tests (placeholder)
	@echo "Tests not implemented yet"

# Production
prod-build: ## Build for production
	docker build -t task-manager-api .

prod-run: ## Run production container
	docker run -d -p 8000:8000 --name task-manager-api task-manager-api 