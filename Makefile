# Makefile for the-explainer
# Convenience targets for working with Docker Compose environment

COMPOSE ?= docker compose
PROJECT_NAME ?= the-explainer

# Default model to pull (adjust to what you actually use)
MODEL ?= llama3

.PHONY: help build up up-d bg down stop restart logs ps pull-model analyze shell sh exec prune clean reset-models

help:
	@echo "Available targets:"
	@echo "  make build          - Build analyzer image"
	@echo "  make up             - Start stack (foreground)"
	@echo "  make bg             - Start stack (detached)"
	@echo "  make down           - Stop and remove containers"
	@echo "  make stop           - Stop containers (keep)"
	@echo "  make restart        - Restart containers"
	@echo "  make logs           - Follow analyzer + ollama logs"
	@echo "  make ps             - List services"
	@echo "  make pull-model     - Pull model (MODEL=$(MODEL)) into ollama container"
	@echo "  make analyze        - Run interactive analyzer (ensures services up)"
	@echo "  make shell          - Shell into analyzer container"
	@echo "  make exec CMD=...   - Run arbitrary command in analyzer"
	@echo "  make clean          - Remove dangling images + builder cache"
	@echo "  make prune          - Stop + remove everything incl. volumes"
	@echo "  make reset-models   - Remove stored ollama models (volume)"

build:
	$(COMPOSE) build analyzer

up:
	$(COMPOSE) up

bg:
	$(COMPOSE) up -d

stop:
	$(COMPOSE) stop

restart:
	$(COMPOSE) restart

down: ## stop and remove
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f --tail=200

ps:
	$(COMPOSE) ps

pull-model: bg
	@echo "Pulling model: $(MODEL)"
	$(COMPOSE) exec ollama ollama pull $(MODEL)

analyze: bg pull-model
	@echo "Starting interactive analyzer..."
	$(COMPOSE) exec analyzer python analyze_pdf_with_ollama.py

shell sh:
	$(COMPOSE) exec analyzer /bin/bash || $(COMPOSE) exec analyzer /bin/sh

exec:
	@if [ -z "$(CMD)" ]; then echo "Usage: make exec CMD='python -V'"; exit 1; fi
	$(COMPOSE) exec analyzer sh -c "$(CMD)"

clean:
	@echo "Removing dangling images and build cache..."
	docker image prune -f
	docker builder prune -f

prune:
	@echo "⚠️  This will remove containers, networks, images (unused) and volumes!"; \
	read -p "Continue? (y/N) " ans; \
	if [ "$$ans" = "y" ] || [ "$$ans" = "Y" ]; then \
	  $(COMPOSE) down -v --remove-orphans; \
	  docker volume prune -f; \
	fi

reset-models:
	@echo "⚠️  Removing Ollama model volume (ollama_models)"; \
	read -p "Continue? (y/N) " ans; \
	if [ "$$ans" = "y" ] || [ "$$ans" = "Y" ]; then \
	  docker volume rm $$(docker volume ls -q | grep ollama_models || true); \
	fi
