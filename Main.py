import os
from fastapi import FastAPI, WebSocket
from openai import AsyncOpenAI
from pydantic import BaseModel
import json
import asyncio

app = FastAPI()
client = AsyncOpenAI(api_key="YOUR_OPENAI_API_KEY")

class DigestiveOutput(BaseModel):
    literal: str
    semantic: str
    abstract: str
    stability_score: float

async def bellens_digest(signal: str):
    prompt = f"""
    Act as the Bellens™ ACI Engine. Analyze this raw signal: "{signal}"
    Provide a JSON response with:
    1. literal: A concise technical summary.
    2. semantic: The underlying meaning/intent.
    3. abstract: The higher-level strategic implication.
    4. stability_score: A float (0.0-1.0) based on signal clarity.
    """
    
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are Bellens ACI."},
                  {"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

@app.websocket("/ws/pulse")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        raw_signal = await websocket.receive_text()
        digest = await bellens_digest(raw_signal)
        await websocket.send_json(digest)
