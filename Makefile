.PHONY: help build start stop logs lint test test-frontend test-backend db-backup

help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build docker containers
	docker-compose build

start: ## Start docker containers in background
	docker-compose up -d

stop: ## Stop docker containers
	docker-compose down

logs: ## Tail docker logs
	docker-compose logs -f

lint: ## Run formatters and linters on backend
	cd backend && PYTHONPATH=.. black .
	cd backend && PYTHONPATH=.. flake8 --max-line-length=120 .
	cd backend && PYTHONPATH=.. mypy --explicit-package-bases --ignore-missing-imports .

test-backend: ## Run backend tests and check coverage
	cd backend && PYTHONPATH=.. coverage run -m pytest tests/
	cd backend && PYTHONPATH=.. coverage report -m --fail-under=58

test-frontend: ## Run frontend tests
	cd frontend && npm run test

test: test-backend test-frontend ## Run all tests

db-backup: ## Backup SQLite database
	@bash backend/scripts/backup_db.sh
