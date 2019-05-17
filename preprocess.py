import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder


class MyPreprocessor(object):
    def __init__(self):
        self.enc = None

    def preprocess(self, data):

        list_col_dummies = [u'Gender', u'Age', u'Occupation',
                            u'City_Category', u'Stay_In_Current_City_Years', u'Marital_Status',
                            u'Product_Category_1']
        X = data.loc[:, list_col_dummies]

        if self.enc is None:
            self.enc = OneHotEncoder(categories='auto', handle_unknown='ignore')
            self.enc.fit(X)


        res = self.enc.transform(X).toarray()

        return pd.DataFrame(res, columns=self.enc.get_feature_names(list_col_dummies))
