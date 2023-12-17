env-active:
	source venv/bin/activate && exec zsh

compose-up:
	docker-compose -f docker-compose.dev.yml up -d

compose-down:
	docker-compose -f docker-compose.dev.yml down -d


.PHONY: env-active compose-up compose-down