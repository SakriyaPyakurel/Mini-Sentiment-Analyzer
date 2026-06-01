from text_utils import BulkTextAnalyzer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score,classification_report
import joblib
class TextClassifier:
    def __init__(self):
        self.model = SVC(kernel='rbf') 
        self.is_trained = False 
    def _prepare_X(self,texts):
        analyzer = BulkTextAnalyzer(texts) 
        df = analyzer.analyze(mode="embeddings") 
        return df.drop(columns=['sentence']).values
    def fit(self,texts,labels):
        X = self._prepare_X(texts)
        self.model.fit(X,labels) 
        self.is_trained = True 
    def predict(self,texts):
        if not self.is_trained:
            raise ValueError("Model not trained yet. Please train the model to use predict") 
        X = self._prepare_X(texts)
        return self.model.predict(X)
    def score(self,test_X,test_Y):
        preds = self.predict(test_X) 
        return accuracy_score(test_Y,preds) 
    def evaluate(self,test_X,test_Y):
        preds = self.predict(test_X) 
        return classification_report(test_Y,preds) 
    def save(self,path_name:str='model.pkl'):
        if not self.is_trained:
          raise ValueError("Model not trained yet. cannot save")
        if not path_name.endswith('.pkl'):
            path_name+='.pkl'
        joblib.dump(self.model,path_name)
    def load(self,path_name:str='model.pkl'):
        self.model = joblib.load(path_name) 
        self.is_trained = True     