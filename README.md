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

Also, make sure the bash scripts are runnable on your local machine:

```
chmod +x ./train_new_model.sh 
chmod +x ./deploy_new_model.sh 
```
#### 1. Preprocessing

```
python dataflow_blackfriday.py  --output gs://artefact-spec-partners-ml/results/output --runner DataflowRunner --project artefact-ml-specialization --temp_location gs://artefact-spec-partners-ml/tmp/
```
The Dataflow pipeline executes the mappings and groupby operations needed to identify VIP Customers.

Input: BlackFriday dataset on BigQuery (click [here](https://console.cloud.google.com/bigquery?project=artefact-ml-specialization&organizationId=495293246545&p=artefact-ml-specialization&d=blackfriday&t=full_dataset&page=table "BigQuery"))

Output: Aggregated data, pushed to BigQuery (click [here](https://console.cloud.google.com/bigquery?project=artefact-ml-specialization&organizationId=495293246545&p=artefact-ml-specialization&d=blackfriday&t=processed_full_data&page=table "BigQuery"))

![Dataflow](https://drive.google.com/uc?export=view&id=1FQ_Z080exLG8cI0PFxln7nNIBzQEfaWo)


This preprocessing has to be done once (not for each training).

#### 2. Training

This command trains the model on the cloud (without hyperparameter tuning at this point, TBD):

```
./train_new_model.sh 

```

Once the job has finished training on the AI platform, the model and the preprocessor have been saved on Cloud Storage here.

You can now create a new version of the serverless model on AI Platform:

```
./deploy_new_model.sh 

```

#### 3. Predicting

Predict whether a potential consumer will be in the top 10% of spenders at the retail store. 

You can type the following in the command line, which will predict 

```
python predict_test.py
```

