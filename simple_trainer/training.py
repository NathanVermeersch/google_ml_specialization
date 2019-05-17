from __future__ import absolute_import
import googleapiclient.discovery
from google.cloud import bigquery
import datetime
import os
import subprocess
import sys
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import pickle
from sklearn.preprocessing import OneHotEncoder
import xgboost as xgb

from past.builtins import unicode

### CONFIG VARIABLES

# Project variables
PROJECT_ID = "artefact-ml-specialization"
BUCKET_NAME = 'artefact-spec-partners-ml'

# Output data directories
train_data_filename = 'train_data.csv'
train_target_filename = 'train_target.csv'
test_data_filename = 'test_data.csv'
test_target_filename = 'test_target.csv'
data_dir = 'gs://artefact-spec-partners-ml/data/blackfriday/config_1'

# Model output directory
model_filename = 'model.joblib'
preprocessor_filename = 'preprocessor.pkl'
model_dir = "blackfriday_model"
gcs_model_path = os.path.join('gs://', BUCKET_NAME, model_dir, model_filename)
gcs_preprocessor_path = os.path.join('gs://', BUCKET_NAME, model_dir, preprocessor_filename)

### AUXILIAR FUNCTIONS
class MyPreprocessor(object):
    def __init__(self):
        self.enc = None

    def preprocess(self, data):

        list_col_dummies = [u'Gender', u'Age', u'Occupation',
                            u'City_Category', u'Stay_In_Current_City_Years', u'Marital_Status',]
        X = data.loc[:, list_col_dummies]

        if self.enc is None:
            self.enc = OneHotEncoder(categories='auto', handle_unknown='ignore')
            self.enc.fit(X)


        res = self.enc.transform(X).toarray()

        return pd.DataFrame(res, columns=self.enc.get_feature_names(list_col_dummies))

### IMPORT DATA

client = bigquery.Client()

# Import train data
train_df=pd.DataFrame({})
query = (
    "SELECT Gender,	Age, Occupation, City_Category,	Stay_In_Current_City_Years,	Marital_Status,	VIP_Purchase FROM "
    "(SELECT *, FARM_FINGERPRINT(CAST(User_ID AS STRING)) AS row_id FROM `blackfriday.processed_full_data` ) "
    "WHERE MOD(ABS(row_id),5) < 4"
)
query_job = client.query(
    query,
    # Location must match that of the dataset(s) referenced in the query.
    location="US",
)  # API request - starts the query
for row in query_job:  # API request - fetches results
    # Row values can be accessed by field name or index
    train_df = train_df.append(dict(row.items()), ignore_index=True)


# Import test data
test_df = pd.DataFrame({})
query = (
    "SELECT Gender,	Age, Occupation,City_Category,	Stay_In_Current_City_Years,	Marital_Status,	VIP_Purchase FROM "
    "(SELECT *, FARM_FINGERPRINT(CAST(User_ID AS STRING)) AS row_id FROM `blackfriday.processed_full_data` ) "
    "WHERE MOD(ABS(row_id),5) = 4"
)
query_job = client.query(
    query,
    # Location must match that of the dataset(s) referenced in the query.
    location="US",
)  # API request - starts the query
for row in query_job:  # API request - fetches results
    # Row values can be accessed by field name or index
    test_df = test_df.append(dict(row.items()), ignore_index=True)


# Save data to GCS

train_data = train_df.drop("VIP_Purchase", axis=1)
train_target = train_df["VIP_Purchase"]
train_data.to_csv(train_data_filename, index=True)
train_target.to_csv(train_target_filename, index=True)

test_data = test_df.drop("VIP_Purchase", axis=1)
test_target = test_df["VIP_Purchase"]
test_data.to_csv(test_data_filename, index=True)
test_target.to_csv(test_target_filename, index=True)

subprocess.check_call(['gsutil', 'cp', train_data_filename, os.path.join(data_dir,
                                                    train_data_filename)], stderr=sys.stdout)
subprocess.check_call(['gsutil', 'cp', train_target_filename, os.path.join(data_dir,
                                                    train_target_filename)], stderr=sys.stdout)

subprocess.check_call(['gsutil', 'cp', test_data_filename, os.path.join(data_dir,
                                                    test_data_filename)], stderr=sys.stdout)
subprocess.check_call(['gsutil', 'cp', test_target_filename, os.path.join(data_dir,
                                                    test_target_filename)], stderr=sys.stdout)

# train_data = train_data.values
# train_target = train_target.values
#
# test_data = test_data.values
# test_target = test_target.values
#
# # Convert one-column 2D array into 1D array for use with XGBoost
# train_target = train_target.reshape((train_target.size,))

# [START train-and-save-model]
# Load data into DMatrix object
# dtrain = xgb.DMatrix(data, label=target)

# Train XGBoost model
# bst = xgb.train({}, dtrain, 20)

### PREPROCESSING

enc = MyPreprocessor()
X = enc.preprocess(train_data)
y = train_target

### MODEL TRAINING

clf = LogisticRegression()
clf.fit(X, y)

print clf.score(X,y)

### EXPORT PREPROCESSOR AND MODEL
# Export the classifier to a file
with open(preprocessor_filename, 'wb') as f:
    pickle.dump(enc, f)
subprocess.check_call(['gsutil', 'cp', preprocessor_filename, gcs_preprocessor_path],
    stderr=sys.stdout)
joblib.dump(clf, model_filename)
subprocess.check_call(['gsutil', 'cp', model_filename, gcs_model_path],
    stderr=sys.stdout)
# bst.save_model(model_filename)
# [END train-and-save-model]


# [START upload-model]
# Upload the saved model file to Cloud Storage

# [END upload-model]

# PROJECT_ID = "artefact-ml-specialization"
# MODEL_NAME = "blackfriday"
# 
# service = googleapiclient.discovery.build('ml', 'v1')
# parent = 'projects/{}/models/{}'.format(PROJECT_ID, MODEL_NAME)
# 
# response = service.projects().models().versions().create(
#     parent=parent,
#     body={
#     "name": datetime.datetime.now().strftime('blackfriday_%Y%m%d_%H%M%S'),
#     "deploymentUri": "gs://artefact-spec-partners-ml/iris_20190515_144146/",
#     "runtimeVersion": "1.13",
#     "framework": "XGBOOST",
#     "pythonVersion": "2.7"
#   }
# ).execute()