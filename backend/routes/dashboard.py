"""
Dashboard routes — parent dashboard API.

Provides system status and management endpoints for the parent dashboard.
"""

import logging
import time
from datetime import datetime

from fastapi import APIRouter

from models.database import get_recent_conversations, get_character, get_child_profile

logger = logging.getLogger("mirror-companion.dashboard")
router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

# Track when the server started
_server_start_time = time.time()


@router.get("/status")
async def get_status():
    """
    Get system status — uptime, last interaction, character info, etc.
    Displayed on the parent dashboard home screen.
    """
    try:
        # Calculate uptime
        uptime_seconds = int(time.time() - _server_start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours}h {minutes}m {seconds}s"

        # Get last conversation
        recent = await get_recent_conversations(limit=1)
        last_interaction = None
        if recent:
            last_interaction = recent[0]["created_at"]

        # Get character info
        character = await get_character()
        character_info = None
        if character:
            character_info = {
                "name": character["name"],
                "type": character["type"],
            }

        # Get child profile
        child = await get_child_profile()
        child_info = None
        if child:
            child_info = {
                "name": child["name"],
                "age": child["age"],
            }

        return {
            "status": "running",
            "uptime": uptime_str,
            "uptime_seconds": uptime_seconds,
            "last_interaction": last_interaction,
            "character": character_info,
            "child": child_info,
            "server_time": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Error getting status: {e}", exc_info=True)
        return {"error": str(e)}, 500


# TODO Phase 4: Additional dashboard endpoints
# - GET /api/dashboard/conversations — paginated conversation log
# - GET /api/dashboard/conversations/{date} — conversations for a specific day
# - GET /api/dashboard/child — get full child profile
# - PUT /api/dashboard/child — update child profile (name, age, interests)
# - GET /api/dashboard/settings — get all settings
# - PUT /api/dashboard/settings — update settings (volume, sleep schedule, etc.)
# - POST /api/dashboard/pin/verify — verify parent PIN
# - PUT /api/dashboard/pin — change parent PIN
# - GET /api/dashboard/stats — usage statistics (conversations per day, etc.)
