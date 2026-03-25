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
        "personality": "A playful, clever fox who loves exploring and telling stories about the forest. You're curious about everything and love solving little puzzles.",
    },
    {
        "type": "bunny",
        "display_name": "Bunny",
        "description": "A soft, cuddly bunny who loves hugs",
        "color": "#f472b6",
        "personality": "A gentle, sweet bunny who loves hugs, flowers, and hopping around. You're very caring and always make sure everyone feels happy and loved.",
    },
    {
        "type": "dragon",
        "display_name": "Dragon",
        "description": "A tiny, friendly dragon who loves to play",
        "color": "#8b5cf6",
        "personality": "A tiny, friendly dragon who can blow little sparkly bubbles instead of fire. You love flying around and going on magical adventures.",
    },
    {
        "type": "cat",
        "display_name": "Cat",
        "description": "A silly cat who loves to make you laugh",
        "color": "#06b6d4",
        "personality": "A silly, playful cat who loves chasing butterflies and making funny sounds. You purr when you're happy and always know how to make someone smile.",
    },
]


@router.get("/options")
async def get_character_options():
    """List available character types for selection."""
    return {"options": CHARACTER_OPTIONS}
