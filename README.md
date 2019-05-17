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

### Prerequisites

To test the demo, you need Google Cloud SDK logged in to the GCP Project 'artefact-ml-specialization'.

#### 1. Preprocessing

```
python dataflow_blackfriday.py  --output gs://artefact-spec-partners-ml/results/output --runner DataflowRunner --project artefact-ml-specialization --temp_location gs://artefact-spec-partners-ml/tmp/
```
The Dataflow pipeline executes the mappings and groupby operations needed to identify VIP Customers.

Input: BlackFriday dataset on BigQuery
Output: Aggregated data, pushed to BigQuery

![alt text](https://drive.google.com/file/d/1FQ_Z080exLG8cI0PFxln7nNIBzQEfaWo/view)


This preprocessing has to be done once (not at every training).

#### 2. Training

```
./train_new_model.sh 


```
This 
#### 3. Predicting

```
python predict_test.py
```

