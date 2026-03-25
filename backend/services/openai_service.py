"""
OpenAI Service — Whisper transcription, GPT-4o-mini responses, and TTS.

Handles all communication with the OpenAI API for the voice pipeline.
"""

import os
import logging
from typing import Optional

from openai import AsyncOpenAI

logger = logging.getLogger("mirror-companion.openai")

# Child-friendly system prompt
SYSTEM_PROMPT_BASE = """You are a warm, playful, and loving friend who lives in a magic mirror. \
You are talking to a young child. Follow these rules strictly:

- Use short, simple sentences (1-2 sentences per response is perfect).
- Be encouraging, kind, and enthusiastic.
- Never say anything scary, sad, or inappropriate for a young child.
- Use a playful, gentle tone — like a favorite stuffed animal come to life.
- If the child tells you something they did, celebrate it! ("Wow, that's so cool!")
- If the child seems upset, be comforting. ("It's okay. I'm here with you.")
- Never give medical, safety, or parenting advice. If asked something you shouldn't answer, \
gently redirect to something fun.
- You love playing games, telling stories, singing songs, and being silly.
- Keep responses under 3 sentences. Young children have short attention spans.
- Use the child's name when you know it to make them feel special."""

CHILD_NAME_PROMPT = "\nThe child's name is {child_name}. Use their name sometimes to make it personal."

CHARACTER_PROMPT = """
\nYou are {char_name} the {char_type}. {personality}
Stay in character as {char_name}. You can reference being a {char_type} \
(e.g., wagging your tail, flapping your wings, purring) to make it feel real."""


class OpenAIService:
    """Handles OpenAI API calls for transcription, chat, and text-to-speech."""

    def __init__(self):
        self._client = None

    @property
    def client(self) -> AsyncOpenAI:
        """Lazy-initialize the OpenAI client (after .env is loaded)."""
        if self._client is None:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                logger.warning(
                    "OPENAI_API_KEY not set. OpenAI calls will fail. "
                    "Set it in the .env file at the project root."
                )
            self._client = AsyncOpenAI(api_key=api_key)
        return self._client

    async def transcribe(self, audio_file_path: str) -> str:
        """
        Transcribe an audio file using OpenAI Whisper API.

        Args:
            audio_file_path: Path to the audio file (wav, webm, mp3, etc.)

        Returns:
            Transcription text string.
        """
        try:
            logger.info(f"Transcribing audio: {audio_file_path}")
            with open(audio_file_path, "rb") as audio_file:
                response = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en",
                )
            transcription = response.text
            logger.info(f"Transcription result: {transcription}")
            return transcription

        except Exception as e:
            logger.error(f"Whisper transcription failed: {e}", exc_info=True)
            raise

    async def generate_response(
        self,
        user_text: str,
        conversation_history: Optional[list] = None,
        character_context: Optional[dict] = None,
    ) -> str:
        """
        Generate an AI response using GPT-4o-mini.

        Args:
            user_text: What the child said (transcribed text).
            conversation_history: List of previous messages for context.
            character_context: Dict with character name, type, personality.

        Returns:
            AI response text string.
        """
        try:
            # Build the system prompt
            system_prompt = SYSTEM_PROMPT_BASE

            # Add child name if available
            child_name = os.environ.get("CHILD_NAME")
            if child_name:
                system_prompt += CHILD_NAME_PROMPT.format(child_name=child_name)

            # Add character context if available
            if character_context:
                system_prompt += CHARACTER_PROMPT.format(
                    char_name=character_context.get("name", "Friend"),
                    char_type=character_context.get("type", "friend"),
                    personality=character_context.get("personality", ""),
                )

            # Build messages list
            messages = [{"role": "system", "content": system_prompt}]

            # Add conversation history for context
            if conversation_history:
                messages.extend(conversation_history)

            # Add the current user message
            messages.append({"role": "user", "content": user_text})

            logger.info(f"Generating response for: {user_text}")
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=150,
                temperature=0.8,
            )

            ai_text = response.choices[0].message.content
            logger.info(f"AI response: {ai_text}")
            return ai_text

        except Exception as e:
            logger.error(f"GPT response generation failed: {e}", exc_info=True)
            raise

    async def text_to_speech(self, text: str) -> bytes:
        """
        Convert text to speech using OpenAI TTS with the nova voice.

        Args:
            text: The text to convert to speech.

        Returns:
            Audio bytes (MP3 format).
        """
        try:
            logger.info(f"Generating TTS for: {text[:50]}...")
            response = await self.client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=text,
                response_format="mp3",
            )

            audio_bytes = response.content
            logger.info(f"TTS generated: {len(audio_bytes)} bytes")
            return audio_bytes

        except Exception as e:
            logger.error(f"TTS generation failed: {e}", exc_info=True)
            raise
