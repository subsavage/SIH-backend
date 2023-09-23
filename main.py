from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

openai.api_key = "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"

# Define the data model for the request payload
class GPTRequest(BaseModel):
    prompt: str

@app.post("/ask/")
async def ask_gpt(request: GPTRequest):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002", 
            prompt=request.prompt,
            max_tokens=100  
        )
        
        gpt_response = response.choices[0].text.strip()
        return {"response": gpt_response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the app, save this code in a file (e.g., `main.py`) and run the following command:
# uvicorn main:app --reload
