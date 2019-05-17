#!/usr/bin/env bash

PROJECT_ID=artefact-ml-specialization
BUCKET_ID=artefact-spec-partners-ml
JOB_NAME=blackfriday_training_$(date +"%Y%m%d_%H%M%S")
JOB_DIR=gs://$BUCKET_ID/blackfriday_job_dir
TRAINING_PACKAGE_PATH="simple_trainer/"
MAIN_TRAINER_MODULE=simple_trainer.training
REGION=europe-west1
RUNTIME_VERSION=1.13
PYTHON_VERSION=2.7
SCALE_TIER=BASIC

gcloud ai-platform jobs submit training $JOB_NAME \
--job-dir $JOB_DIR \
--package-path $TRAINING_PACKAGE_PATH \
--module-name $MAIN_TRAINER_MODULE \
--region $REGION \
--runtime-version=$RUNTIME_VERSION \
--python-version=$PYTHON_VERSION \
--scale-tier $SCALE_TIER