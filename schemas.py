from pydantic import BaseModel 
#Request schema
class TextRequest(BaseModel):
    texts:list[str] 
#Response schema
class PredictionResponse(BaseModel):
    predictions:list[int]

class csv_generator_request(BaseModel):
    pathname:str 

class csv_generator_response(BaseModel):
    message:str