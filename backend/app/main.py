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
