HOST := raspberrypi.local
SSH_USER := pi
SSH_KEY := ~/.ssh/pi-key
CRON := */10 * * * *

.EXPORT_ALL_VARIABLES:

.PHONY: provision
provision: build
	docker compose run --rm ansible

.PHONY: shell
shell: build
	docker compose run --entrypoint '' --rm ansible bash

.PHONY: build
build:
	docker compose build ansible
