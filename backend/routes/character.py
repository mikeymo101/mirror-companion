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


# TODO Phase 2: Additional character endpoints
# - PUT /api/character/{id} — update character name or personality
# - GET /api/character/options — list available character types with previews
# - POST /api/character/animation — trigger a specific animation state
# - GET /api/character/mood — get current character mood
