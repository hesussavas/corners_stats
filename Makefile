PG_CONTAINER_NAME ?= corners-postgres
POSTGRES_DB ?= corners
POSTGRES_USER ?= corners
POSTGRES_PASSWORD = corners


test-psql-run:
	-docker run -d \
		-e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
		-e POSTGRES_USER=$(POSTGRES_USER)\
		-e POSTGRES_DB=$(POSTGRES_DB)\
		-p 8432:5432 \
		--name $(PG_CONTAINER_NAME) \
		postgres:9.5


bash-build:
	docker build \
		--file=Dockerfile \
		-t corners/bash:dev \
		.


start_scraping: bash-build test-psql-run
	sleep 2
	docker run --rm -i \
		--link $(PG_CONTAINER_NAME) \
		-e DEV_PSQL_URI=postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(PG_CONTAINER_NAME):5432/$(POSTGRES_DB) \
		corners/bash:dev \
		./start.sh


db_init: bash-build test-psql-run
	sleep 2
	docker run --rm -i \
		--link $(PG_CONTAINER_NAME) \
		-e DEV_PSQL_URI=postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(PG_CONTAINER_NAME):5432/$(POSTGRES_DB) \
		corners/bash:dev \
		./db_init.sh

analysis: bash-build test-psql-run
	sleep 2
	docker run --rm -i \
		--link $(PG_CONTAINER_NAME) \
		--volume $(CURDIR)/files/:/opt/corners/files/ \
		-e DEV_PSQL_URI=postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(PG_CONTAINER_NAME):5432/$(POSTGRES_DB) \
		corners/bash:dev \
		python3 analysis.py
