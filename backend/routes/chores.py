"""
Chores routes — placeholder for Phase 5.

Chore management, morning routines, and tracking will be built here.
"""

import logging
from fastapi import APIRouter

logger = logging.getLogger("mirror-companion.chores")
router = APIRouter(prefix="/api/chores", tags=["chores"])


@router.get("")
async def get_chores():
    """
    Get all chores for the child.

    TODO Phase 5:
    - Query chores table from database
    - Include completion status for today
    - Include streak information
    - Filter by frequency (daily, weekly, etc.)
    """
    return {
        "chores": [],
        "message": "Chore tracking coming in Phase 5!",
    }


@router.post("")
async def create_chore():
    """
    Create a new chore.

    TODO Phase 5:
    - Accept chore details: name, description, frequency, time_of_day
    - Save to database
    - Support recurring schedules (daily, specific days, weekly)
    - Set reminder times
    """
    return {
        "message": "Chore creation coming in Phase 5!",
    }


# TODO Phase 5: Additional chore endpoints
# - PUT /api/chores/{id} — update a chore
# - DELETE /api/chores/{id} — remove a chore
# - POST /api/chores/{id}/complete — mark a chore as done (voice or dashboard)
# - GET /api/chores/today — get today's chore checklist
# - GET /api/chores/streaks — get streak data for celebrations
# - GET /api/chores/routine/morning — get morning routine sequence
# - POST /api/chores/routine/morning/start — trigger morning routine on mirror
