import os
import pickle

import numpy as np
from sklearn.datasets import load_iris
from sklearn.externals import joblib
import pandas as pd
import sys


class MyPredictor(object):
    def __init__(self, model, preprocessor):
        self._model = model
        self._preprocessor = preprocessor
        self._class_names = load_iris().target_names

    def predict(self, instances, **kwargs):
        cols = [u'Gender', u'Age', u'Occupation',
                u'City_Category', u'Stay_In_Current_City_Years', u'Marital_Status']
        inputs = pd.DataFrame(instances, columns=cols)
        preprocessed_inputs = self._preprocessor.preprocess(inputs)
        # if kwargs.get('probabilities'):
        #   probabilities = self._model.predict_proba(preprocessed_inputs)
        #   return probabilities.tolist()
        #
        try:
            outputs = self._model.predict(preprocessed_inputs)
            return str(outputs)
        except Exception as e:
            msg = str(e)
            return str(msg)

    @classmethod
    def from_path(cls, model_dir):
        model_path = os.path.join(model_dir, 'model.joblib')
        model = joblib.load(model_path)

        preprocessor_path = os.path.join(model_dir, 'preprocessor.pkl')
        with open(preprocessor_path, 'rb') as f:
            preprocessor = pickle.load(f)

        return cls(model, preprocessor)
