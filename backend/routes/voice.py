"""
Voice routes — speech-to-text, AI response with skills, text-to-speech pipeline.
"""

import os
import json
import base64
import logging
import tempfile
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from services.openai_service import OpenAIService
from models.database import save_conversation, get_recent_conversations, get_character
from skills.registry import skill_registry

logger = logging.getLogger("mirror-companion.voice")
router = APIRouter(prefix="/api/voice", tags=["voice"])

openai_service = OpenAIService()

TEMP_AUDIO_DIR = os.path.join(tempfile.gettempdir(), "mirror-companion-audio")
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)


async def execute_skill(name: str, args: dict) -> str:
    """Execute a skill by name. Used as callback for OpenAI tool calls."""
    skill = skill_registry.get(name)
    if skill:
        return await skill.execute(**args)
    return f"Unknown skill: {name}"


async def get_ai_context():
    """Get character context and conversation history for AI calls."""
    character = await get_character()
    character_context = None
    if character:
        character_context = {
            "name": character["name"],
            "type": character["type"],
            "personality": character["personality"],
        }

    recent = await get_recent_conversations(limit=5)
    conversation_history = []
    for conv in recent:
        conversation_history.append({"role": "user", "content": conv["user_text"]})
        conversation_history.append({"role": "assistant", "content": conv["ai_text"]})

    return character, character_context, conversation_history


class SpeakRequest(BaseModel):
    text: str


class ConversationResponse(BaseModel):
    transcription: str
    response_text: str
    audio_url: str


@router.post("/listen")
async def listen(audio: UploadFile = File(...)):
    """Transcribe audio with Whisper."""
    temp_path = None
    try:
        suffix = Path(audio.filename).suffix if audio.filename else ".webm"
        temp_path = os.path.join(TEMP_AUDIO_DIR, f"{uuid.uuid4()}{suffix}")
        content = await audio.read()
        with open(temp_path, "wb") as f:
            f.write(content)
        transcription = await openai_service.transcribe(temp_path)
        return {"transcription": transcription}
    except Exception as e:
        logger.error(f"Error in /listen: {e}", exc_info=True)
        return {"error": str(e)}, 500
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@router.post("/speak")
async def speak(request: SpeakRequest):
    """Text → AI response → TTS audio."""
    try:
        character, character_context, conversation_history = await get_ai_context()
        tools = skill_registry.get_all_tool_definitions()

        response_text = await openai_service.generate_response(
            user_text=request.text,
            conversation_history=conversation_history,
            character_context=character_context,
            tools=tools if tools else None,
            skill_executor=execute_skill,
        )
        audio_bytes = await openai_service.text_to_speech(response_text)

        character_id = character["id"] if character else None
        await save_conversation(request.text, response_text, character_id)

        return StreamingResponse(
            iter([audio_bytes]),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=response.mp3"},
        )
    except Exception as e:
        logger.error(f"Error in /speak: {e}", exc_info=True)
        return {"error": str(e)}, 500


@router.post("/conversation", response_model=ConversationResponse)
async def conversation(audio: UploadFile = File(...)):
    """Full pipeline: audio → transcription → AI response → TTS."""
    temp_audio_path = None
    try:
        suffix = Path(audio.filename).suffix if audio.filename else ".webm"
        temp_audio_path = os.path.join(TEMP_AUDIO_DIR, f"{uuid.uuid4()}{suffix}")
        content = await audio.read()
        with open(temp_audio_path, "wb") as f:
            f.write(content)

        transcription = await openai_service.transcribe(temp_audio_path)
        character, character_context, conversation_history = await get_ai_context()
        tools = skill_registry.get_all_tool_definitions()

        response_text = await openai_service.generate_response(
            user_text=transcription,
            conversation_history=conversation_history,
            character_context=character_context,
            tools=tools if tools else None,
            skill_executor=execute_skill,
        )

        audio_bytes = await openai_service.text_to_speech(response_text)
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_output_path = os.path.join(TEMP_AUDIO_DIR, audio_filename)
        with open(audio_output_path, "wb") as f:
            f.write(audio_bytes)

        character_id = character["id"] if character else None
        await save_conversation(transcription, response_text, character_id)

        return ConversationResponse(
            transcription=transcription,
            response_text=response_text,
            audio_url=f"/api/voice/audio/{audio_filename}",
        )
    except Exception as e:
        logger.error(f"Error in /conversation: {e}", exc_info=True)
        return {"error": str(e)}, 500
    finally:
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)


@router.get("/audio/{filename}")
async def get_audio(filename: str):
    """Serve a generated audio file."""
    file_path = os.path.join(TEMP_AUDIO_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "Audio file not found"}, 404

    def iter_file():
        with open(file_path, "rb") as f:
            yield f.read()
        os.remove(file_path)

    return StreamingResponse(
        iter_file(),
        media_type="audio/mpeg",
        headers={"Content-Disposition": f"inline; filename={filename}"},
    )


@router.websocket("/ws")
async def voice_websocket(websocket: WebSocket):
    """WebSocket for real-time voice interaction with skill support."""
    await websocket.accept()
    logger.info("WebSocket connected.")

    try:
        while True:
            message = await websocket.receive()

            # Handle disconnect
            if message.get("type") == "websocket.disconnect":
                break

            # Parse audio data
            if "text" in message:
                try:
                    payload = json.loads(message["text"])
                    if payload.get("type") != "audio" or not payload.get("audio"):
                        continue
                    audio_data = base64.b64decode(payload["audio"])
                except (json.JSONDecodeError, Exception):
                    continue
            elif "bytes" in message:
                audio_data = message["bytes"]
            else:
                continue

            # Process voice pipeline
            temp_path = os.path.join(TEMP_AUDIO_DIR, f"{uuid.uuid4()}.webm")
            try:
                with open(temp_path, "wb") as f:
                    f.write(audio_data)

                logger.info(f"Received {len(audio_data)} bytes of audio")

                # Transcribe
                transcription = await openai_service.transcribe(temp_path)
                logger.info(f"Transcription: '{transcription}'")

                if not transcription or not transcription.strip():
                    await websocket.send_json({"type": "silence", "message": "No speech detected"})
                    continue

                # Get context
                character, character_context, conversation_history = await get_ai_context()
                tools = skill_registry.get_all_tool_definitions()

                # Generate response (with skill support)
                response_text = await openai_service.generate_response(
                    user_text=transcription,
                    conversation_history=conversation_history,
                    character_context=character_context,
                    tools=tools if tools else None,
                    skill_executor=execute_skill,
                )

                # Generate TTS
                audio_bytes = await openai_service.text_to_speech(response_text)

                # Save to DB
                character_id = character["id"] if character else None
                await save_conversation(transcription, response_text, character_id)

                # Send response
                await websocket.send_json({
                    "type": "response",
                    "transcription": transcription,
                    "response_text": response_text,
                })
                await websocket.send_bytes(audio_bytes)
                logger.info("Response sent.")

            except Exception as e:
                logger.error(f"Processing error: {e}", exc_info=True)
                try:
                    await websocket.send_json({"type": "error", "message": str(e)})
                except Exception:
                    break
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
