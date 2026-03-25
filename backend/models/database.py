"""
Database — SQLite via aiosqlite for async access.

Manages all persistent data: character info, conversations, and child profile.
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional

import aiosqlite

logger = logging.getLogger("mirror-companion.database")

# Database file lives in the backend directory
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "mirror_companion.db")


async def _get_db() -> aiosqlite.Connection:
    """Get a database connection with row factory enabled."""
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    return db


async def init_db():
    """
    Create all tables if they don't exist.
    Called on application startup.
    """
    logger.info(f"Initializing database at {DB_PATH}")
    db = await _get_db()
    try:
        await db.executescript(
            """
            CREATE TABLE IF NOT EXISTS character (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                personality TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_text TEXT NOT NULL,
                ai_text TEXT NOT NULL,
                character_id INTEGER,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (character_id) REFERENCES character(id)
            );

            CREATE TABLE IF NOT EXISTS child_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                birthday TEXT,
                interests TEXT DEFAULT '[]',
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            """
        )
        await db.commit()
        logger.info("Database tables created/verified successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}", exc_info=True)
        raise
    finally:
        await db.close()


# --- Character ---


async def get_character() -> Optional[dict]:
    """
    Get the current character from the database.
    Returns the most recently created character, or None if no character exists.
    """
    db = await _get_db()
    try:
        cursor = await db.execute(
            "SELECT id, name, type, personality, created_at "
            "FROM character ORDER BY created_at DESC LIMIT 1"
        )
        row = await cursor.fetchone()
        if row is None:
            return None
        return {
            "id": row["id"],
            "name": row["name"],
            "type": row["type"],
            "personality": row["personality"],
            "created_at": row["created_at"],
        }
    except Exception as e:
        logger.error(f"Error fetching character: {e}", exc_info=True)
        raise
    finally:
        await db.close()


async def save_character(name: str, character_type: str, personality: str) -> int:
    """
    Save a new character to the database.

    Args:
        name: The name the child gave the character.
        character_type: Type of character (fox, bunny, dragon, cat).
        personality: Personality description for the AI prompt.

    Returns:
        The new character's ID.
    """
    db = await _get_db()
    try:
        cursor = await db.execute(
            "INSERT INTO character (name, type, personality) VALUES (?, ?, ?)",
            (name, character_type, personality),
        )
        await db.commit()
        character_id = cursor.lastrowid
        logger.info(f"Character saved: {name} the {character_type} (id={character_id})")
        return character_id
    except Exception as e:
        logger.error(f"Error saving character: {e}", exc_info=True)
        raise
    finally:
        await db.close()


# --- Conversations ---


async def save_conversation(
    user_text: str, ai_text: str, character_id: Optional[int] = None
) -> int:
    """
    Save a conversation exchange to the database.

    Args:
        user_text: What the child said (transcribed).
        ai_text: What the AI responded.
        character_id: ID of the active character (optional).

    Returns:
        The new conversation record's ID.
    """
    db = await _get_db()
    try:
        cursor = await db.execute(
            "INSERT INTO conversations (user_text, ai_text, character_id) VALUES (?, ?, ?)",
            (user_text, ai_text, character_id),
        )
        await db.commit()
        return cursor.lastrowid
    except Exception as e:
        logger.error(f"Error saving conversation: {e}", exc_info=True)
        raise
    finally:
        await db.close()


async def get_recent_conversations(limit: int = 10) -> list:
    """
    Get the most recent conversations, ordered newest first.

    Args:
        limit: Maximum number of conversations to return.

    Returns:
        List of conversation dicts.
    """
    db = await _get_db()
    try:
        cursor = await db.execute(
            "SELECT id, user_text, ai_text, character_id, created_at "
            "FROM conversations ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )
        rows = await cursor.fetchall()
        # Return in chronological order (oldest first) for conversation context
        conversations = [
            {
                "id": row["id"],
                "user_text": row["user_text"],
                "ai_text": row["ai_text"],
                "character_id": row["character_id"],
                "created_at": row["created_at"],
            }
            for row in reversed(rows)
        ]
        return conversations
    except Exception as e:
        logger.error(f"Error fetching conversations: {e}", exc_info=True)
        raise
    finally:
        await db.close()


# --- Child Profile ---


async def get_child_profile() -> Optional[dict]:
    """
    Get the child's profile from the database.
    Returns the first profile, or None if not set up yet.
    """
    db = await _get_db()
    try:
        cursor = await db.execute(
            "SELECT id, name, age, birthday, interests, created_at, updated_at "
            "FROM child_profile LIMIT 1"
        )
        row = await cursor.fetchone()
        if row is None:
            return None

        # Parse interests JSON
        interests = []
        try:
            interests = json.loads(row["interests"]) if row["interests"] else []
        except json.JSONDecodeError:
            interests = []

        return {
            "id": row["id"],
            "name": row["name"],
            "age": row["age"],
            "birthday": row["birthday"],
            "interests": interests,
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
    except Exception as e:
        logger.error(f"Error fetching child profile: {e}", exc_info=True)
        raise
    finally:
        await db.close()


async def save_child_profile(
    name: str,
    age: Optional[int] = None,
    birthday: Optional[str] = None,
    interests: Optional[list] = None,
) -> int:
    """
    Save or update the child's profile.

    If a profile already exists, updates it. Otherwise creates a new one.

    Args:
        name: Child's name.
        age: Child's age.
        birthday: Birthday string (e.g., "2023-03-15").
        interests: List of interest strings.

    Returns:
        The profile ID.
    """
    interests_json = json.dumps(interests or [])
    now = datetime.now().isoformat()

    db = await _get_db()
    try:
        # Check if a profile already exists
        cursor = await db.execute("SELECT id FROM child_profile LIMIT 1")
        existing = await cursor.fetchone()

        if existing:
            # Update existing profile
            await db.execute(
                "UPDATE child_profile SET name=?, age=?, birthday=?, interests=?, updated_at=? "
                "WHERE id=?",
                (name, age, birthday, interests_json, now, existing["id"]),
            )
            await db.commit()
            logger.info(f"Child profile updated: {name}")
            return existing["id"]
        else:
            # Create new profile
            cursor = await db.execute(
                "INSERT INTO child_profile (name, age, birthday, interests) VALUES (?, ?, ?, ?)",
                (name, age, birthday, interests_json),
            )
            await db.commit()
            profile_id = cursor.lastrowid
            logger.info(f"Child profile created: {name} (id={profile_id})")
            return profile_id
    except Exception as e:
        logger.error(f"Error saving child profile: {e}", exc_info=True)
        raise
    finally:
        await db.close()
