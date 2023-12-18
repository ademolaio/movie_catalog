env-active:
	source venv/bin/activate && exec zsh

compose-up:
	docker-compose -f docker-compose.yml up -d

compose-down:
	docker-compose -f docker-compose.yml down -d


.PHONY: env-active compose-up compose-down