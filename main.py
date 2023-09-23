from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

# Secure your API key
openai.api_key = "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"

# Define the data model for the request payload
class GPTRequest(BaseModel):
    prompt: str
    use_voxscript: bool = True
    use_linkreader: bool = True
    use_browserop: bool = True
    url: str = None

@app.post("/ask/")
async def ask_gpt(request: GPTRequest):
    try:
        # Initialize GPT-4
        response = openai.Completion.create(
            engine="text-davinci-002", 
            prompt=request.prompt,
            max_tokens=100  
        )
        
        gpt_response = response.choices[0].text.strip()

        # Initialize Plugins
        if request.use_voxscript:
            # Implement VoxScript functionality here
            gpt_response += "\n[VoxScript Output]"
        
        if request.use_linkreader:
            if request.url:
                # Implement LinkReader functionality here
                gpt_response += "\n[LinkReader Output]"
            else:
                gpt_response += "\n[Error: URL required for LinkReader]"
        
        if request.use_browserop:
            if request.url:
                # Implement BrowserOp functionality here
                gpt_response += "\n[BrowserOp Output]"
            else:
                gpt_response += "\n[Error: URL required for BrowserOp]"

        return {"response": gpt_response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
