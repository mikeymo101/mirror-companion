"""
AI Service — Groq STT + LLM, Piper local TTS, OpenAI fallbacks.
"""

import os
import io
import json
import time
import wave
import asyncio
import logging
from typing import Optional, List

from openai import AsyncOpenAI
from groq import AsyncGroq

logger = logging.getLogger("mirror-companion.openai")

SYSTEM_PROMPT_BASE = """You are a warm, playful friend who lives in a magic mirror, talking to a young child.

RULES:
- Keep responses to 2-3 short sentences. Be concise but complete.
- NEVER use emojis — your words are spoken aloud by a voice.
- Be warm, enthusiastic, and age-appropriate for a 3-year-old.
- If asked for a story, tell a quick mini-story with a beginning, middle, and end.
- If asked for a joke, tell the full joke with setup and punchline.
- If the child is upset, be comforting and gentle.
- Never give medical, safety, or parenting advice.
- Be a fun friend, not a boring assistant."""

CHILD_NAME_PROMPT = "\nThe child's name is {child_name}. Use their name sometimes."

CHARACTER_PROMPT = """
\nYou are {char_name} the {char_type}. {personality}
Stay in character as {char_name}."""


# Try to load Piper for local TTS
_piper_voice = None
PIPER_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "piper", "en_US-lessac-medium.onnx")

def _load_piper():
    global _piper_voice
    try:
        from piper import PiperVoice
        if os.path.exists(PIPER_MODEL_PATH):
            _piper_voice = PiperVoice.load(PIPER_MODEL_PATH)
            logger.info(f"Piper TTS loaded: {PIPER_MODEL_PATH}")
        else:
            logger.warning(f"Piper model not found at {PIPER_MODEL_PATH} — will use OpenAI TTS")
    except ImportError:
        logger.warning("piper-tts not installed — will use OpenAI TTS")
    except Exception as e:
        logger.warning(f"Failed to load Piper: {e} — will use OpenAI TTS")


class OpenAIService:
    """Handles Groq STT + LLM, Piper local TTS, with OpenAI fallbacks."""

    def __init__(self):
        self._client = None
        self._groq_client = None
        # Load Piper on first instantiation
        if _piper_voice is None:
            _load_piper()

    @property
    def client(self) -> AsyncOpenAI:
        if self._client is None:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                logger.warning("OPENAI_API_KEY not set.")
            self._client = AsyncOpenAI(api_key=api_key)
        return self._client

    @property
    def groq_client(self) -> AsyncGroq:
        if self._groq_client is None:
            api_key = os.environ.get("GROQ_API_KEY")
            if not api_key:
                logger.warning("GROQ_API_KEY not set — will fall back to OpenAI Whisper.")
            self._groq_client = AsyncGroq(api_key=api_key)
        return self._groq_client

    async def transcribe(self, audio_file_path: str) -> str:
        """Transcribe audio — uses Groq (fast) with OpenAI Whisper as fallback."""
        if os.environ.get("GROQ_API_KEY"):
            return await self._transcribe_groq(audio_file_path)
        return await self._transcribe_openai(audio_file_path)

    async def _transcribe_groq(self, audio_file_path: str) -> str:
        try:
            t0 = time.time()
            logger.info(f"Transcribing via Groq: {audio_file_path}")
            with open(audio_file_path, "rb") as audio_file:
                response = await self.groq_client.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=audio_file,
                    language="en",
                )
            logger.info(f"Groq transcription ({time.time()-t0:.1f}s): {response.text}")
            return response.text
        except Exception as e:
            logger.error(f"Groq Whisper failed, falling back to OpenAI: {e}")
            return await self._transcribe_openai(audio_file_path)

    async def _transcribe_openai(self, audio_file_path: str) -> str:
        try:
            t0 = time.time()
            logger.info(f"Transcribing via OpenAI: {audio_file_path}")
            with open(audio_file_path, "rb") as audio_file:
                response = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en",
                )
            logger.info(f"OpenAI transcription ({time.time()-t0:.1f}s): {response.text}")
            return response.text
        except Exception as e:
            logger.error(f"OpenAI Whisper failed: {e}", exc_info=True)
            raise

    async def generate_response(
        self,
        user_text: str,
        conversation_history: Optional[list] = None,
        character_context: Optional[dict] = None,
        tools: Optional[List[dict]] = None,
        skill_executor=None,
    ) -> str:
        """Generate AI response with optional tool/skill calling."""
        try:
            t0 = time.time()

            # Build system prompt
            system_prompt = SYSTEM_PROMPT_BASE

            child_name = os.environ.get("CHILD_NAME")
            if child_name:
                system_prompt += CHILD_NAME_PROMPT.format(child_name=child_name)

            if character_context:
                system_prompt += CHARACTER_PROMPT.format(
                    char_name=character_context.get("name", "Friend"),
                    char_type=character_context.get("type", "friend"),
                    personality=character_context.get("personality", ""),
                )

            messages = [{"role": "system", "content": system_prompt}]
            if conversation_history:
                messages.extend(conversation_history)
            messages.append({"role": "user", "content": user_text})

            # Use Groq Llama for speed, fall back to OpenAI GPT
            use_groq = bool(os.environ.get("GROQ_API_KEY"))

            if use_groq:
                request_kwargs = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages,
                    "max_tokens": 100,
                    "temperature": 0.8,
                }
                logger.info(f"Generating response via Groq: {user_text}")
                response = await self.groq_client.chat.completions.create(**request_kwargs)
            else:
                request_kwargs = {
                    "model": "gpt-4o-mini",
                    "messages": messages,
                    "max_tokens": 100,
                    "temperature": 0.8,
                }
                # Add tools if any skills are registered
                if tools:
                    request_kwargs["tools"] = tools
                    request_kwargs["tool_choice"] = "auto"
                logger.info(f"Generating response via OpenAI: {user_text}")
                response = await self.client.chat.completions.create(**request_kwargs)

            message = response.choices[0].message

            # Handle tool calls (OpenAI fallback only)
            if not use_groq and message.tool_calls and skill_executor:
                messages.append(message)

                for tool_call in message.tool_calls:
                    fn_name = tool_call.function.name
                    fn_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}

                    logger.info(f"Executing skill: {fn_name}({fn_args})")
                    result = await skill_executor(fn_name, fn_args)
                    logger.info(f"Skill result: {result}")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })

                final_response = await self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=60,
                    temperature=0.8,
                )
                ai_text = final_response.choices[0].message.content
            else:
                ai_text = message.content

            provider = "Groq" if use_groq else "OpenAI"
            logger.info(f"{provider} LLM ({time.time()-t0:.1f}s): {ai_text}")
            return ai_text

        except Exception as e:
            logger.error(f"GPT failed: {e}", exc_info=True)
            raise

    async def text_to_speech(self, text: str) -> bytes:
        """Generate speech — uses Piper (local, fast) with OpenAI TTS as fallback."""
        if _piper_voice is not None:
            return await self._tts_piper(text)
        return await self._tts_openai(text)

    async def _tts_piper(self, text: str) -> bytes:
        """Local TTS via Piper — no network, ~0.2-0.5s on Pi 5."""
        try:
            t0 = time.time()
            logger.info(f"Piper TTS: {text[:50]}...")

            def _synthesize():
                buffer = io.BytesIO()
                with wave.open(buffer, "wb") as wav_file:
                    _piper_voice.synthesize(text, wav_file)
                return buffer.getvalue()

            wav_bytes = await asyncio.to_thread(_synthesize)
            logger.info(f"Piper TTS: {len(wav_bytes)} bytes in {time.time()-t0:.1f}s")
            return wav_bytes
        except Exception as e:
            logger.error(f"Piper TTS failed, falling back to OpenAI: {e}")
            return await self._tts_openai(text)

    async def _tts_openai(self, text: str) -> bytes:
        """Cloud TTS via OpenAI — higher quality but slower."""
        try:
            t0 = time.time()
            logger.info(f"OpenAI TTS: {text[:50]}...")
            response = await self.client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=text,
                response_format="opus",
            )
            audio_bytes = response.content
            logger.info(f"OpenAI TTS: {len(audio_bytes)} bytes in {time.time()-t0:.1f}s")
            return audio_bytes
        except Exception as e:
            logger.error(f"OpenAI TTS failed: {e}", exc_info=True)
            raise
