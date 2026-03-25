"""
Voice routes — speech-to-text, AI response, text-to-speech pipeline.
"""

import os
import logging
import tempfile
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from services.openai_service import OpenAIService
from models.database import save_conversation, get_recent_conversations, get_character

logger = logging.getLogger("mirror-companion.voice")
router = APIRouter(prefix="/api/voice", tags=["voice"])

openai_service = OpenAIService()

# Directory for temporary audio files
TEMP_AUDIO_DIR = os.path.join(tempfile.gettempdir(), "mirror-companion-audio")
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)


class SpeakRequest(BaseModel):
    text: str


class ConversationResponse(BaseModel):
    transcription: str
    response_text: str
    audio_url: str


@router.post("/listen")
async def listen(audio: UploadFile = File(...)):
    """
    Accept an audio file upload (webm/wav), transcribe it with Whisper.
    Returns the transcription text.
    """
    temp_path = None
    try:
        # Save uploaded audio to a temp file
        suffix = Path(audio.filename).suffix if audio.filename else ".webm"
        temp_path = os.path.join(TEMP_AUDIO_DIR, f"{uuid.uuid4()}{suffix}")

        content = await audio.read()
        with open(temp_path, "wb") as f:
            f.write(content)

        # Transcribe with Whisper
        transcription = await openai_service.transcribe(temp_path)

        return {"transcription": transcription}

    except Exception as e:
        logger.error(f"Error in /listen: {e}", exc_info=True)
        return {"error": str(e)}, 500

    finally:
        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@router.post("/speak")
async def speak(request: SpeakRequest):
    """
    Accept text, generate AI response with GPT-4o-mini, convert to speech
    with OpenAI TTS (nova voice), return audio as streaming MP3 response.
    """
    try:
        # Get character context for the system prompt
        character = await get_character()
        character_context = None
        if character:
            character_context = {
                "name": character["name"],
                "type": character["type"],
                "personality": character["personality"],
            }

        # Get recent conversation history for context
        recent = await get_recent_conversations(limit=10)
        conversation_history = [
            {"role": "user", "content": c["user_text"]}
            if i % 2 == 0
            else {"role": "assistant", "content": c["ai_text"]}
            for i, c in enumerate(recent)
        ]

        # Generate AI response
        response_text = await openai_service.generate_response(
            user_text=request.text,
            conversation_history=conversation_history,
            character_context=character_context,
        )

        # Generate TTS audio
        audio_bytes = await openai_service.text_to_speech(response_text)

        # Save conversation to DB
        character_id = character["id"] if character else None
        await save_conversation(request.text, response_text, character_id)

        # Stream back as MP3
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
    """
    Full voice pipeline: accept audio upload, transcribe, generate AI response,
    save TTS audio to a temp file, return JSON with transcription, response text,
    and a URL to the audio file.
    """
    temp_audio_path = None
    try:
        # Save uploaded audio to temp file
        suffix = Path(audio.filename).suffix if audio.filename else ".webm"
        temp_audio_path = os.path.join(TEMP_AUDIO_DIR, f"{uuid.uuid4()}{suffix}")

        content = await audio.read()
        with open(temp_audio_path, "wb") as f:
            f.write(content)

        # Step 1: Transcribe
        transcription = await openai_service.transcribe(temp_audio_path)
        logger.info(f"Transcription: {transcription}")

        # Step 2: Get character context
        character = await get_character()
        character_context = None
        if character:
            character_context = {
                "name": character["name"],
                "type": character["type"],
                "personality": character["personality"],
            }

        # Step 3: Get conversation history
        recent = await get_recent_conversations(limit=10)
        conversation_history = []
        for conv in recent:
            conversation_history.append({"role": "user", "content": conv["user_text"]})
            conversation_history.append(
                {"role": "assistant", "content": conv["ai_text"]}
            )

        # Step 4: Generate AI response
        response_text = await openai_service.generate_response(
            user_text=transcription,
            conversation_history=conversation_history,
            character_context=character_context,
        )
        logger.info(f"AI response: {response_text}")

        # Step 5: Generate TTS audio and save to temp file
        audio_bytes = await openai_service.text_to_speech(response_text)
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_output_path = os.path.join(TEMP_AUDIO_DIR, audio_filename)
        with open(audio_output_path, "wb") as f:
            f.write(audio_bytes)

        # Step 6: Save conversation to DB
        character_id = character["id"] if character else None
        await save_conversation(transcription, response_text, character_id)

        # Return the audio URL (served from temp dir, frontend fetches it)
        audio_url = f"/api/voice/audio/{audio_filename}"

        return ConversationResponse(
            transcription=transcription,
            response_text=response_text,
            audio_url=audio_url,
        )

    except Exception as e:
        logger.error(f"Error in /conversation: {e}", exc_info=True)
        return {"error": str(e)}, 500

    finally:
        # Clean up input audio temp file
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)


@router.get("/audio/{filename}")
async def get_audio(filename: str):
    """Serve a generated audio file from the temp directory."""
    file_path = os.path.join(TEMP_AUDIO_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "Audio file not found"}, 404

    def iter_file():
        with open(file_path, "rb") as f:
            yield f.read()
        # Clean up after serving
        os.remove(file_path)

    return StreamingResponse(
        iter_file(),
        media_type="audio/mpeg",
        headers={"Content-Disposition": f"inline; filename={filename}"},
    )


@router.websocket("/ws")
async def voice_websocket(websocket: WebSocket):
    """
    WebSocket for real-time voice interaction.
    Receives audio chunks from the client, processes them,
    and sends back AI responses.
    """
    await websocket.accept()
    logger.info("WebSocket connection established.")

    try:
        while True:
            # Receive audio data from client (JSON with base64 audio or raw bytes)
            message = await websocket.receive()

            if "text" in message:
                # JSON message with base64 audio from browser
                import json
                import base64
                payload = json.loads(message["text"])
                if payload.get("type") != "audio" or not payload.get("audio"):
                    continue
                audio_data = base64.b64decode(payload["audio"])
            elif "bytes" in message:
                # Raw bytes
                audio_data = message["bytes"]
            else:
                continue

            # Save received audio to temp file
            temp_path = os.path.join(TEMP_AUDIO_DIR, f"{uuid.uuid4()}.webm")
            with open(temp_path, "wb") as f:
                f.write(audio_data)

            try:
                # Transcribe
                transcription = await openai_service.transcribe(temp_path)

                if not transcription or transcription.strip() == "":
                    await websocket.send_json(
                        {"type": "silence", "message": "No speech detected"}
                    )
                    continue

                # Get character context
                character = await get_character()
                character_context = None
                if character:
                    character_context = {
                        "name": character["name"],
                        "type": character["type"],
                        "personality": character["personality"],
                    }

                # Get conversation history
                recent = await get_recent_conversations(limit=5)
                conversation_history = []
                for conv in recent:
                    conversation_history.append(
                        {"role": "user", "content": conv["user_text"]}
                    )
                    conversation_history.append(
                        {"role": "assistant", "content": conv["ai_text"]}
                    )

                # Generate response
                response_text = await openai_service.generate_response(
                    user_text=transcription,
                    conversation_history=conversation_history,
                    character_context=character_context,
                )

                # Generate TTS
                audio_bytes = await openai_service.text_to_speech(response_text)

                # Save conversation
                character_id = character["id"] if character else None
                await save_conversation(transcription, response_text, character_id)

                # Send transcription text
                await websocket.send_json(
                    {
                        "type": "response",
                        "transcription": transcription,
                        "response_text": response_text,
                    }
                )

                # Send audio bytes
                await websocket.send_bytes(audio_bytes)

            finally:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
        await websocket.close(code=1011, reason=str(e))
