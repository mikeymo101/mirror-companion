"""
Mirror Companion App — FastAPI Backend Entry Point

Raspberry Pi 5 magic mirror voice companion for children.
"""

import os
import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.database import init_db
from skills.registry import skill_registry
from routes.voice import router as voice_router
from routes.character import router as character_router
from routes.chores import router as chores_router
from routes.dashboard import router as dashboard_router

# Load .env from project root (one level up from backend/)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("mirror-companion")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("Starting Mirror Companion backend...")
    logger.info(f"GROQ_API_KEY: {'set (' + os.environ.get('GROQ_API_KEY', '')[:8] + '...)' if os.environ.get('GROQ_API_KEY') else 'NOT SET'}")
    logger.info(f"OPENAI_API_KEY: {'set' if os.environ.get('OPENAI_API_KEY') else 'NOT SET'}")
    await init_db()
    logger.info("Database initialized.")
    skill_registry.auto_discover()
    logger.info(f"Skills loaded: {skill_registry.list_skills()}")
    yield
    logger.info("Shutting down Mirror Companion backend.")


app = FastAPI(
    title="Mirror Companion",
    description="Voice companion backend for the magic mirror",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allow all origins for local network access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(voice_router)
app.include_router(character_router)
app.include_router(chores_router)
app.include_router(dashboard_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "mirror-companion",
        "skills": skill_registry.list_skills(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_excludes=["*.db", "*.sqlite"],
        log_level="info",
    )
