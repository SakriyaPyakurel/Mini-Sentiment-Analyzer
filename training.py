from raw_data import data,labels 
from sklearn.model_selection import train_test_split 
from text_classify import TextClassifier 
classifier = TextClassifier() 
X_train,X_test,Y_train,Y_test = train_test_split(data,labels,test_size=0.3,random_state=42) 
classifier.fit(X_train,Y_train) 
score = classifier.score(X_test,Y_test) 
print(score) 
if score > 0.8:
    classifier.save('text_classifier_model') 
else:
    print('Model accuracy is below 80. Cannot save') 
print(classifier.evaluate(X_test,Y_test)) 