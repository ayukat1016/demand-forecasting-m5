ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yaml
VERSION := 1.0.0

DOCKER_REPOSITORY := demand_forecasting_m5

DIR := $(ABSOLUTE_PATH)
TAG = demand_forecasting_m5
PLATFORM := linux/amd64


############ DEMAND FORECASTING DATA_REGISTRATION COMMANDS ############
DATA_REGISTRATION_DIR := $(DIR)/data_registration
DOCKERFILE_DATA_REGISTRATION = $(DATA_REGISTRATION_DIR)/$(DOCKERFILE)
DOCKER_DATA_REGISTRATION_TAG = $(TAG)_data_registration
DOCKER_DATA_REGISTRATION_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_DATA_REGISTRATION_TAG)_$(VERSION)

.PHONY: req_data_registration
req_data_registration:
	cd $(DATA_REGISTRATION_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_data_registration
build_data_registration:
	docker build \
		--platform $(PLATFORM) \
		-t $(DOCKER_DATA_REGISTRATION_IMAGE_NAME) \
		-f $(DOCKERFILE_DATA_REGISTRATION) \
		.

.PHONY: push_data_registration
push_data_registration:
	docker push $(DOCKER_DATA_REGISTRATION_IMAGE_NAME)

.PHONY: pull_data_registration
pull_data_registration:
	docker pull $(DOCKER_DATA_REGISTRATION_IMAGE_NAME)


############ DEMAND FORECASTING MLFLOW COMMANDS ############
MLFLOW_DIR := $(DIR)/mlflow
DOCKERFILE_MLFLOW = $(MLFLOW_DIR)/$(DOCKERFILE)
DOCKER_MLFLOW_TAG = $(TAG)_mlflow
DOCKER_MLFLOW_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_MLFLOW_TAG)_$(VERSION)

.PHONY: req_mlflow
req_mlflow:
	cd $(MLFLOW_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_mlflow
build_mlflow:
	docker build \
		--platform $(PLATFORM) \
		-t $(DOCKER_MLFLOW_IMAGE_NAME) \
		-f $(DOCKERFILE_MLFLOW) \
		.

.PHONY: push_mlflow
push_mlflow:
	docker push $(DOCKER_MLFLOW_IMAGE_NAME)

.PHONY: pull_mlflow
pull_mlflow:
	docker pull $(DOCKER_MLFLOW_IMAGE_NAME)


############ DEMAND FORECASTING MACHINE_LEARNING COMMANDS ############
MACHINE_LEARNING_DIR := $(DIR)/machine_learning
DOCKERFILE_MACHINE_LEARNING = $(MACHINE_LEARNING_DIR)/$(DOCKERFILE)
DOCKER_MACHINE_LEARNING_TAG = $(TAG)_machine_learning
DOCKER_MACHINE_LEARNING_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_MACHINE_LEARNING_TAG)_$(VERSION)

.PHONY: req_machine_learning
req_machine_learning:
	cd $(MACHINE_LEARNING_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_machine_learning
build_machine_learning:
	docker build \
		--platform $(PLATFORM) \
		-t $(DOCKER_MACHINE_LEARNING_IMAGE_NAME) \
		-f $(DOCKERFILE_MACHINE_LEARNING) \
		.

.PHONY: run_machine_learning
run_machine_learning:
	docker run \
		-it \
		--name machine_learning \
		-e POSTGRES_HOST=postgres \
		-e POSTGRES_PORT=5432 \
		-e POSTGRES_USER=postgres \
		-e POSTGRES_PASSWORD=password \
		-e POSTGRES_DBNAME=demand_forecasting_m5 \
		-e MLFLOW_TRACKING_URI=http://mlflow:5000 \
		-e TARGET_CONFIG=default \
		-v $(MACHINE_LEARNING_DIR)/hydra:/opt/hydra \
		-v $(MACHINE_LEARNING_DIR)/src:/opt/src \
		-v $(MACHINE_LEARNING_DIR)/outputs:/opt/outputs \
		--net demand_forecasting_m5 \
		$(DOCKER_MACHINE_LEARNING_IMAGE_NAME) \
		python -m src.main

.PHONY: push_machine_learning
push_machine_learning:
	docker push $(DOCKER_MACHINE_LEARNING_IMAGE_NAME)

.PHONY: pull_machine_learning
pull_machine_learning:
	docker pull $(DOCKER_MACHINE_LEARNING_IMAGE_NAME)


############ DEMAND FORECASTING BI COMMANDS ############
BI_DIR := $(DIR)/bi
DOCKERFILE_BI = $(BI_DIR)/$(DOCKERFILE)
DOCKER_BI_TAG = $(TAG)_bi
DOCKER_BI_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_BI_TAG)_$(VERSION)

.PHONY: req_bi
req_bi:
	cd $(BI_DIR) && \
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: build_bi
build_bi:
	docker build \
		--platform $(PLATFORM) \
		-t $(DOCKER_BI_IMAGE_NAME) \
		-f $(DOCKERFILE_BI) \
		.

.PHONY: run_bi
run_bi:
	docker run \
		-it \
		--name bi \
		-e POSTGRES_HOST=postgres \
		-e POSTGRES_PORT=5432 \
		-e POSTGRES_USER=postgres \
		-e POSTGRES_PASSWORD=password \
		-e POSTGRES_DBNAME=demand_forecasting_m5 \
		-p 8501:8501 \
		-v $(BI_DIR)/src:/opt/src \
		--net demand_forecasting_m5 \
		$(DOCKER_BI_IMAGE_NAME) \
		streamlit run src/main.py

.PHONY: push_bi
push_bi:
	docker push $(DOCKER_BI_IMAGE_NAME)

.PHONY: pull_bi
pull_bi:
	docker pull $(DOCKER_BI_IMAGE_NAME)


############ ALL COMMANDS ############
.PHONY: req_all
req_all: req_data_registration \
	req_machine_learning \
	req_mlflow \

.PHONY: build_all
build_all: build_data_registration \
	build_machine_learning \
	build_mlflow \
	build_bi \

.PHONY: push_all
push_all: push_data_registration \
	push_machine_learning \
	push_mlflow \

.PHONY: pull_all
pull_all: pull_data_registration \
	pull_machine_learning \
	pull_mlflow \


############ DOCKER COMPOSE COMMANDS ############
.PHONY: up
up:
	docker compose \
		-f $(DOCKER_COMPOSE) \
		up -d

.PHONY: down
down:
	docker compose \
		-f $(DOCKER_COMPOSE) \
		down
