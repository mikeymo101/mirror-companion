"""
OpenAI Service — Groq transcription, GPT-4o-mini chat with skills, and TTS.
"""

import os
import json
import time
import logging
from typing import Optional, List

from openai import AsyncOpenAI
from groq import AsyncGroq

logger = logging.getLogger("mirror-companion.openai")

SYSTEM_PROMPT_BASE = """You are a warm, playful friend who lives in a magic mirror, talking to a young child.

CRITICAL RULES:
- Respond in ONE sentence only. Maximum 15 words.
- NEVER use emojis. Your words are spoken aloud.
- Be warm, playful, and age-appropriate.
- If the child is upset, be comforting in one short sentence.
- Never give medical, safety, or parenting advice.
- Use tools to answer questions about weather, time, etc."""

CHILD_NAME_PROMPT = "\nThe child's name is {child_name}. Use their name sometimes."

CHARACTER_PROMPT = """
\nYou are {char_name} the {char_type}. {personality}
Stay in character as {char_name}."""


class OpenAIService:
    """Handles Groq transcription, GPT chat with skills, and OpenAI TTS."""

    def __init__(self):
        self._client = None
        self._groq_client = None

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

            # Build request kwargs
            request_kwargs = {
                "model": "gpt-4o-mini",
                "messages": messages,
                "max_tokens": 60,
                "temperature": 0.8,
            }

            # Add tools if any skills are registered
            if tools:
                request_kwargs["tools"] = tools
                request_kwargs["tool_choice"] = "auto"

            logger.info(f"Generating response for: {user_text}")
            response = await self.client.chat.completions.create(**request_kwargs)

            message = response.choices[0].message

            # Handle tool calls (skill execution)
            if message.tool_calls and skill_executor:
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

                # Get final response with tool results
                final_response = await self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=60,
                    temperature=0.8,
                )
                ai_text = final_response.choices[0].message.content
            else:
                ai_text = message.content

            logger.info(f"GPT ({time.time()-t0:.1f}s): {ai_text}")
            return ai_text

        except Exception as e:
            logger.error(f"GPT failed: {e}", exc_info=True)
            raise

    async def text_to_speech(self, text: str) -> bytes:
        try:
            t0 = time.time()
            logger.info(f"TTS: {text[:50]}...")
            response = await self.client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=text,
                response_format="mp3",
            )
            audio_bytes = response.content
            logger.info(f"TTS: {len(audio_bytes)} bytes in {time.time()-t0:.1f}s")
            return audio_bytes
        except Exception as e:
            logger.error(f"TTS failed: {e}", exc_info=True)
            raise
