from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
from fastapi.responses import JSONResponse

app=FastAPI()
handler=Mangum(app)

class Text(BaseModel):
    string: str

@app.post("/")
def convert_string_to_lowercase(text: Text):
    return JSONResponse({"converted_string":text.string.lower()})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
