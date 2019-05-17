# google_ml_specialization
Google Cloud ML Partners Specialization

This repository contains the provisional version of the code for the demo of Assessment 2 (dealing with the Black Friday dataset).

The main functionalities identified in the requirements are the following:

* Preprocess the data using Dataflow (chosen among Dataflow, BigQuery and Dataproc)
* Train a model on AI Platform (hyperparameter tuning has not been implemented yet)
* Online prediction using the AI platform API and the model previously trained


Here, the business goal we established is finding new potential VIP users, that is users that would be ready to spend more than 90 % of other customers.

As a result, the initial preprocessing is done through Dataflow and consists of aggregating the sum of purchases by users, and then creating a binary label equal to 1 if the total purchase accounts for more than the 90th percentile.

This reduces simply to a binary classification problem.

1. Preprocessing

```
python dataflow_blackfriday.py  --output gs://artefact-spec-partners-ml/results/output --runner DataflowRunner --project artefact-ml-specialization --temp_location gs://artefact-spec-partners-ml/tmp/
```

This has to be done once (not at every training).

2. Training

```
./train_new_model.sh 


```

3. Predicting

```
python predict_test.py
```

