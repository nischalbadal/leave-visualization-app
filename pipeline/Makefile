# Set the shell to bash
SHELL := /bin/bash
IMAGE_NAME := data-pipeline
ENV_FILE := ../.env  # Path to the .env file

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Clean up dangling Docker images
cleanup:
	docker image prune -f

# Run the extraction process with the API source
ingestion-api: build
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) extraction.py --source=api
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) validation.py --type=ingestion

# Run the extraction process with the file upload source
ingestion-bulk: build
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) extraction.py --source=upload --file=../files/vyaguta-api-response.json
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) validation.py --type=ingestion

# Run the transformation process
transformation: build
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) transformation.py
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) validation.py --type=transformation

# Run the data transfer process
data-transfer: build
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) data-transfer.py
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) validation.py --type=data-transfer

# Run the ETL process for API data
etl-api: build
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) extraction.py --source=api
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) validation.py --type=ingestion
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) transformation.py
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) validation.py --type=transformation
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) data-transfer.py
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) validation.py --type=data-transfer
	make cleanup

# Run the ETL process for Bulk file upload
etl-bulk: build
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) extraction.py --source=upload --file=../files/vyaguta-api-response.json
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) validation.py --type=ingestion
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) transformation.py
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) validation.py --type=transformation
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) data-transfer.py
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) validation.py --type=data-transfer
	make cleanup