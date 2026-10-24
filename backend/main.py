from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

# This allows Godot to talk to your server locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PullRequest(BaseModel):
    player_wallet: str

@app.post("/gacha/pull")
async def process_gacha_pull(req: PullRequest):
    names = ["Aria the 404 Error", "Null-chan", "Syntax Error-tan", "Infinite Loop Lily"]
    personalities = ["Tsundere", "Overly caffeinated", "Procrastinator", "Extremely dramatic"]
    
    selected_name = random.choice(names)
    selected_p = random.choice(personalities)

    return {
        "status": "success",
        "wallet": req.player_wallet,
        "character": {
            "name": selected_name,
            "personality": selected_p,
            "affection": 0,
            "greeting": f"Ugh, why did you summon me? I'm {selected_name} and I'm a {selected_p}."
        }
    }
