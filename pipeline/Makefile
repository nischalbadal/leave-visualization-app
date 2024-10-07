# Set the shell to bash
SHELL := /bin/bash
IMAGE_NAME := data-pipeline
ENV_FILE := ../.env  # Path to the .env file

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the extraction process with the API source
ingestion-api: build
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) extraction.py --source=api

# Run the extraction process with the file upload source
ingestion-bulk: build
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) extraction.py --source=upload --file=../files/vyaguta-api-response.json

# Run the transformation process
transformation: build
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) transformation.py

# Run the transformation process
data-transfer: build
	docker run --env-file $(ENV_FILE) --env DB_HOST=host.docker.internal $(IMAGE_NAME) data-transfer.py
