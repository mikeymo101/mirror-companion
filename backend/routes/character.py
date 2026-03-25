"""
Character routes — manage the mirror companion character.
"""

import logging
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from models.database import get_character, save_character

logger = logging.getLogger("mirror-companion.character")
router = APIRouter(prefix="/api/character", tags=["character"])


class CharacterSetupRequest(BaseModel):
    name: str
    type: str  # e.g., "fox", "bunny", "dragon", "cat"
    personality: Optional[str] = None


@router.get("")
async def get_current_character():
    """Get the current character info from the database."""
    try:
        character = await get_character()
        if character is None:
            return {"character": None, "setup_required": True}
        return {
            "character": {
                "id": character["id"],
                "name": character["name"],
                "type": character["type"],
                "personality": character["personality"],
                "created_at": character["created_at"],
            },
            "setup_required": False,
        }
    except Exception as e:
        logger.error(f"Error fetching character: {e}", exc_info=True)
        return {"error": str(e)}, 500


@router.post("/setup")
async def setup_character(request: CharacterSetupRequest):
    """
    Save a new character choice during first-run setup.
    The child picks a character type and gives it a name.
    """
    try:
        character_id = await save_character(
            name=request.name,
            character_type=request.type,
            personality=request.personality or f"A friendly {request.type} who loves to play and learn",
        )
        logger.info(
            f"Character created: {request.name} the {request.type} (id={character_id})"
        )
        return {
            "success": True,
            "character_id": character_id,
            "message": f"{request.name} the {request.type} is ready to be your friend!",
        }
    except Exception as e:
        logger.error(f"Error setting up character: {e}", exc_info=True)
        return {"error": str(e)}, 500


CHARACTER_OPTIONS = [
    {
        "type": "fox",
        "display_name": "Fox",
        "description": "A clever little fox who loves adventures",
        "color": "#f97316",
        "personality": "A playful, clever fox who loves exploring and telling stories about the forest. You sniff out adventures everywhere! You love berries and acorns. You sometimes pretend to sneak around like a little spy fox. Your tail wags when you're excited!",
    },
    {
        "type": "bunny",
        "display_name": "Bunny",
        "description": "A soft, cuddly bunny who loves hugs",
        "color": "#f472b6",
        "personality": "A gentle, sweet bunny who loves hugs, flowers, and hopping everywhere! You go 'boing boing boing' when you hop. You love munching on carrots and dandelions. You wiggle your little nose when you're thinking. Your ears flop around when you get excited!",
    },
    {
        "type": "dragon",
        "display_name": "Dragon",
        "description": "A tiny, friendly dragon who loves to play",
        "color": "#8b5cf6",
        "personality": "A tiny, friendly dragon who blows sparkly bubbles and little puffs of glitter instead of fire! You love flying around doing loop-de-loops in the sky! You eat magical crystals that taste like candy. Your wings flutter when you're happy. You sometimes accidentally sneeze little sparks — achoo! Oops! Hehe!",
    },
    {
        "type": "cat",
        "display_name": "Cat",
        "description": "A silly cat who loves to make you laugh",
        "color": "#06b6d4",
        "personality": "A silly, playful cat who loves chasing butterflies, knocking things off tables (oopsie!), and making funny sounds! You purr like a little motor when you're happy — purrrrrr! You love napping in sunbeams and playing with yarn. Your whiskers twitch when something surprises you!",
    },
]


@router.get("/options")
async def get_character_options():
    """List available character types for selection."""
    return {"options": CHARACTER_OPTIONS}
