"""
Voice routes — speech-to-text, AI response with skills, text-to-speech pipeline.
"""

import os
import json
import base64
import logging
import tempfile
import time
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
    """WebSocket for real-time voice interaction with skill support.

    Accepts two message types:
    - {"type": "text", "text": "..."} — pre-transcribed text from browser SpeechRecognition (fast path)
    - {"type": "audio", "audio": "base64..."} — raw audio for Whisper transcription (fallback)
    """
    await websocket.accept()
    logger.info("WebSocket connected.")

    try:
        while True:
            message = await websocket.receive()

            if message.get("type") == "websocket.disconnect":
                break

            # Parse incoming message
            transcription = None
            temp_path = None

            if "text" in message:
                try:
                    payload = json.loads(message["text"])

                    if payload.get("type") == "text" and payload.get("text"):
                        # Fast path: browser already transcribed the speech
                        transcription = payload["text"].strip()
                        logger.info(f"Received text (browser STT): '{transcription}'")

                    elif payload.get("type") == "audio" and payload.get("audio"):
                        # Fallback: decode audio and transcribe with Whisper
                        audio_data = base64.b64decode(payload["audio"])
                        temp_path = os.path.join(TEMP_AUDIO_DIR, f"{uuid.uuid4()}.webm")
                        with open(temp_path, "wb") as f:
                            f.write(audio_data)
                        logger.info(f"Received {len(audio_data)} bytes of audio, transcribing...")
                        transcription = await openai_service.transcribe(temp_path)
                        logger.info(f"Whisper transcription: '{transcription}'")
                    else:
                        continue

                except (json.JSONDecodeError, Exception) as e:
                    logger.error(f"Failed to parse message: {e}")
                    continue
            elif "bytes" in message:
                audio_data = message["bytes"]
                temp_path = os.path.join(TEMP_AUDIO_DIR, f"{uuid.uuid4()}.webm")
                with open(temp_path, "wb") as f:
                    f.write(audio_data)
                transcription = await openai_service.transcribe(temp_path)
            else:
                continue

            # Process the transcription
            try:
                if not transcription or not transcription.strip():
                    await websocket.send_json({"type": "silence", "message": "No speech detected"})
                    continue

                t_start = time.time()

                # Get context and generate response
                character, character_context, conversation_history = await get_ai_context()
                tools = skill_registry.get_all_tool_definitions()

                # Stream GPT response and TTS each sentence as it arrives
                logger.info("Streaming AI response...")
                full_response = ""
                first_audio = True

                async for sentence in openai_service.generate_response_streaming(
                    user_text=transcription,
                    conversation_history=conversation_history,
                    character_context=character_context,
                    tools=tools if tools else None,
                    skill_executor=execute_skill,
                ):
                    full_response += (" " + sentence if full_response else sentence)
                    t_gpt = time.time()
                    logger.info(f"GPT sentence ({t_gpt-t_start:.1f}s): '{sentence}'")

                    # Send the text response on first chunk so UI updates fast
                    if first_audio:
                        await websocket.send_json({
                            "type": "response",
                            "transcription": transcription,
                            "response_text": sentence,
                        })
                        first_audio = False

                    # Generate and send TTS for this sentence
                    audio_bytes = await openai_service.text_to_speech(sentence)
                    await websocket.send_bytes(audio_bytes)
                    logger.info(f"Sent audio chunk ({time.time()-t_gpt:.1f}s TTS)")

                # Save to DB
                character_id = character["id"] if character else None
                await save_conversation(transcription, full_response, character_id)

                t_total = time.time() - t_start
                logger.info(f"Total pipeline: {t_total:.1f}s")

            except Exception as e:
                logger.error(f"Processing error: {e}", exc_info=True)
                try:
                    await websocket.send_json({"type": "error", "message": str(e)})
                except Exception:
                    break
            finally:
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
