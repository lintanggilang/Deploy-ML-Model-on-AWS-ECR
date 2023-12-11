# Import necessary libraries
import os
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from mangum import Mangum

app = FastAPI()

# Directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the model file
MODEL_PATH = os.path.join(BASE_DIR, 'model.sav')

# Load the model
model = pickle.load(open(MODEL_PATH, 'rb'))

def umur(x):
    if x <= 12:
        return "1"
    elif x >= 13 and x <= 18:
        return "2"
    elif x >= 19 and x <= 40:
        return "3"
    elif x >= 41 and x <= 65:
        return "4"    
    else:
        return "5"

class Passenger(BaseModel):
    Pclass: int = Field(example=3)
    Sex: str = Field(example="male")
    Age: float = Field(example=22.0)
    SibSp: int = Field(example=1)
    Parch: int = Field(example=0)
    Fare: float = Field(example=7.25)
    Embarked: str = Field(example="S")

@app.get("/")
def read_root():
    return {"Hello": "Titanic"}

@app.post("/")
def predict_survival(passenger: Passenger):
    try:
        # Create DataFrame
        df = pd.DataFrame([dict(passenger)])

        # Apply the 'umur' function
        df['umur'] = df['Age'].apply(lambda x : umur(x))
        df['WA'] = 0
        df.loc[(df['umur'] == '1') | (df['Sex'] == 'female'), 'WA'] = 1

        # Predict
        prediction = model.predict(df)
        result = {"Survived": int(prediction[0])}
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# This will be the entry point for AWS Lambda
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
