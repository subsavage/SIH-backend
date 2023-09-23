from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import json
import re

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

# Function to extract relevant URLs
def extract_relevant_urls(text):
    urls = re.findall(r'https?://\S+', text)
    return urls

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

        # Extract relevant URLs
        relevant_urls = extract_relevant_urls(gpt_response)

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

        return {"response": gpt_response, "relevant_urls": relevant_urls}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))