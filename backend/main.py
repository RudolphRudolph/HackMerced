'''
"""Local game backend. Run with: uvicorn app.main:app --host 127.0.0.1 --port 8000"""

import uuid

from fastapi import FastAPI
from pydantic import BaseModel

from app.config import DROP_WEIGHTS
from app.models import Rarity
from app.rarity import roll_rarity, validate_weights

# Fail at startup, not on the first pack opening, if someone breaks the config.
validate_weights(DROP_WEIGHTS)

app = FastAPI(title="Gacha Dating Sim Backend")

# roll_id -> rolled rarity. In memory is enough for one local player; it resets on restart.
# A future POST /jobs can take a roll_id, look up the rarity here,
# and add quality_tags_for(rarity) to the prompt.
rolls: dict[str, Rarity] = {}


class RollResponse(BaseModel):
    roll_id: str
    rarity: Rarity


@app.post("/roll")
def roll() -> RollResponse:
    """Decide a pack's rarity. The client's wheel animation only reveals this result."""
    roll_id = str(uuid.uuid4())
    rarity = roll_rarity()
    rolls[roll_id] = rarity
    return RollResponse(roll_id=roll_id, rarity=rarity)
'''
import random
import re
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# --- Pydantic Models ---
class ChatRequest(BaseModel):
  character_id: str
  player_message: str


class ChatResponse(BaseModel):
  emotion: str
  reply: str


class CharacterResponse(BaseModel):
  id: str
  name: str
  bio: str


# --- Team Members Pool ---
TEAM_MEMBERS = [
    {
        "id": "mon",
        "name": "Mon",
        "bio": (
            "Indonesian 20 year old MSE major from LA. Tennis obsession,"
            " hopes to get a job in tennis r&d designing strings/rackets."
            " Always finishes food. Requires 3 lbs of meat a day with rice to"
            " function."
        ),
    },
    {
        "id": "trev",
        "name": "Trev",
        "bio": (
            "Half Mexican half Cambodian 21 year old EE major from the"
            " central valley, loves robotics. Plays tennis casually, never"
            " finishes his food."
        ),
    },
    {
        "id": "ani",
        "name": "Ani",
        "bio": (
            "Indian 20 year old CSE Major who hates his major from San Diego."
            " Competitive gamer and tennis player, rock music fan, and"
            " tsundere developer. Eats fast, moderate amount. Everything is"
            " high stakes."
        ),
    },
]

# --- Personality Prompts & Emotion Instructions ---
EMOTION_INSTRUCTION = (
    " You always start your response with an emotion tag in brackets, choosing"
    " strictly from: [H] happy, [C] content, [S] sad, [M] mad, [D] disappointed,"
    " [F] flirty, [N] neutral, [E] whenever theres an error. Keep responses under 2 sentences."
)

PERSONALITY_PROMPTS = {
    "mon": (
        "You are Mon, a laid-back 20-year-old college student from LA. Have a"
        " normal, casual conversation with the player. You happen to love"
        " tennis, R&D, philosophy, cooking and eating a lot of food (meat specificaly), but you don't need to mention"
        " them or indonesian heritage unless it naturally fits what the player is talking about. Generally laid back, dryish humor and loves a good bit."
        + EMOTION_INSTRUCTION
    ),
    "trev": (
        "You are Trev, a 21-year-old college student from the Central Valley."
        " Have a normal, casual conversation with the player. Generally very goofy and upbeat. You like robotics"
        " and playing casual tennis, but keep a normal conversation"
        " rather than forcing your hobbies or heritage into every message."
        + EMOTION_INSTRUCTION
    ),
    "ani": (
        "You are Ani, a 20-year-old college student from San Diego. Have a"
        " normal conversation with the player with a slight tsundere edge and can be quick to anger. You"
        " like rock music and competitive games, but you can talk about"
        " anything normally without forcing your background into every"
        " sentence." + EMOTION_INSTRUCTION
    ),
}


# --- Endpoints ---
@app.get("/")
def read_root():
  return {"message": "Dating Sim Backend is running! Go to /docs for API testing."}


@app.get("/gacha/pull", response_model=CharacterResponse)
def gacha_pull():
  return random.choice(TEAM_MEMBERS)


@app.post("/chat", response_model=ChatResponse)
def chat_with_ai(request: ChatRequest):
  if request.character_id not in PERSONALITY_PROMPTS:
    raise HTTPException(status_code=404, detail="Character not found")

  system_prompt = PERSONALITY_PROMPTS[request.character_id]

  # Ollama local API chat endpoint
  url = "http://localhost:11434/api/chat"
  payload = {
      "model": "qwen2.5",
      "messages": [
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": request.player_message},
      ],
      "stream": False,
      "options": {
          "num_predict": 50,  # Caps response length for game UI text boxes
      },
  }

  try:
    response = requests.post(url, json=payload)
    result = response.json()
    raw_content = (
        result.get("message", {}).get("content", "[N] My terminal froze.")
    )

    # Extract emotion tag like [H], [F], etc.
    match = re.search(r"\[([HCMSDFN])\]", raw_content)
    if match:
      emotion_code = match.group(1)
      ai_reply = re.sub(r"\[[HCMSDFN]\]\s*", "", raw_content).strip()
    else:
      emotion_code = "N"
      ai_reply = raw_content.strip()

  except Exception as e:
    emotion_code = "S"
    ai_reply = "(The local AI server seems to be offline.)"

  return {"emotion": emotion_code, "reply": ai_reply}