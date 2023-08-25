from typing import Any

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from .model import process_user_input

import time

app = FastAPI()

# This defines the data json format expected for the endpoint, change as needed
class TextInput(BaseModel):
    inputs: str
    parameters: dict[str, Any] | None

@app.get("/")
def read_root():
    return {"message": "Hello, Welcome to Reacto chatbot API!"}

@app.post("/generate/")
async def generate_text(data: TextInput) -> dict[str, str]:
    try:
        time_start = time.time()
        query = data.inputs
        response = process_user_input(query)
        result = response['answer']
        time_elapsed = time.time() - time_start
        return {"generated_text": result, "query": query, "response_time": "{:.2f}".format(time_elapsed)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))