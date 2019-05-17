#!/usr/bin/env bash

gsutil cp gs://artefact-spec-partners-ml/blackfriday_model/preprocessor.pkl preprocessor.pkl
gsutil cp gs://artefact-spec-partners-ml/blackfriday_model/model.joblib model.joblib

python setup.py sdist --formats=gztar

export BUCKET_NAME=artefact-spec-partners-ml

gsutil cp ./dist/my_custom_code-0.1.tar.gz gs://$BUCKET_NAME/custom_prediction_routine_tutorial/my_custom_code-0.1.tar.gz
gsutil cp model.joblib preprocessor.pkl gs://$BUCKET_NAME/custom_prediction_routine_tutorial/model/

gcloud beta ai-platform versions create $VERSION_NAME   --model $MODEL_NAME   --runtime-version 1.13   --python-version 2.7   --origin gs://$BUCKET_NAME/custom_prediction_routine_tutorial/model/   --package-uris gs://$BUCKET_NAME/custom_prediction_routine_tutorial/my_custom_code-0.1.tar.gz   --prediction-class predictor.MyPredictor