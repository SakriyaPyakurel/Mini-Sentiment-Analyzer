from fastapi import FastAPI,HTTPException
from text_classify import TextClassifier
from contextlib import asynccontextmanager
from schemas import TextRequest,PredictionResponse,csv_generator_request,csv_generator_response
import os
import re
import pandas as pd
BASE_DIR = 'outputs'
os.makedirs(BASE_DIR,exist_ok=True)
@asynccontextmanager
async def lifecycle(app:FastAPI):
    #startup
    app.state.classifier = TextClassifier() 
    app.state.predictions = []
    try:
        app.state.classifier.load('text_classifier_model.pkl') 
        print("Model loaded successfully") 
    except Exception as e:
        print(f'Model loading failed: {e}') 
    yield

app = FastAPI(lifespan=lifecycle)

@app.get('/') 
def home():
    return {"message":"Text classification API is up and running"} 

@app.post('/predict',response_model=PredictionResponse) 
def predict(request:TextRequest):
    classifier = app.state.classifier 
    if not classifier.is_trained:
        raise HTTPException(status_code=400,detail='Model not trained') 
    preds = classifier.predict(request.texts) 
    preds_list = preds.tolist()
    app.state.predictions.extend([{'sentence':s,'label':l} for s,l in zip(request.texts,preds_list)])
    return {"status":"success","predictions":preds_list}

@app.post('/generate_csv',response_model=csv_generator_response) 
def generate_csv(request:csv_generator_request):
    predictions = app.state.predictions
    if len(predictions) == 0:
        raise HTTPException(status_code=400,detail='No predictions available to save') 
    else:
        pathname = re.sub(r'[^a-zA-Z0-9_.-]', '_', request.pathname) if request.pathname else 'output_file.csv'
        filename = os.path.basename(pathname) 
        filepath = os.path.join(BASE_DIR,filename)
        if not filepath.endswith('.csv'):
            filepath+='.csv' 
        file_exists = os.path.isfile(filepath) and os.path.getsize(filepath) > 0
        df = pd.DataFrame(predictions) 
        df.to_csv(filepath,mode='a',header=not file_exists,index=False)
        app.state.predictions.clear()
        return {'message':f'Saved successfully','file':filename}
            
                









