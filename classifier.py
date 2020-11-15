from sklearn import svm
from sklearn.neural_network import MLPClassifier

import pandas as pd

class Classifier:
    def __init__(self,file_name):
        self.file_name = file_name
        self.clf = MLPClassifier((2, ), random_state = 0, learning_rate_init = 0.01, activation = "logistic")

    def get_data(self):
        self.data = pd.read_csv(self.file_name,index_col=False)
        self.classes = self.data.iloc[:,6]
        self.attributes = self.data.iloc[:,:6]
    
    def fit(self):
        self.clf.fit(self.attributes.values,self.classes)
    
    def predict(self,value):
        return self.clf.predict(value)