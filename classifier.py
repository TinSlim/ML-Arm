from sklearn import svm
import pandas as pd

class classifier:
    def __init__(self,file_name):
        self.file_name = file_name
        self.clf = svm.SVC()

    def get_data(self):
        self.data = pd.read_csv(self.file_name,index_col=False)
        self.classes = data.iloc[:,6]
        self.attributes = data.iloc[:,:6]
    
    def fit(self):
        self.clf.fit(self.attributes.values,self.classes)
    
    def predict(self,value)
        return self.clf.predict(value)