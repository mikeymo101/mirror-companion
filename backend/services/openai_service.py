"""
OpenAI Service — Whisper transcription, GPT-4o-mini with skills, and TTS.
"""

import os
import json
import time
import logging
from typing import Optional, List, AsyncGenerator

from openai import AsyncOpenAI

logger = logging.getLogger("mirror-companion.openai")

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
- Use the child's name when you know it to make them feel special.
- You have special abilities (tools) you can use to get information like weather and time. \
Use them when the child asks about these things instead of making up answers."""

CHILD_NAME_PROMPT = "\nThe child's name is {child_name}. Use their name sometimes to make it personal."

CHARACTER_PROMPT = """
\nYou are {char_name} the {char_type}. {personality}
Stay in character as {char_name}. You can reference being a {char_type} \
(e.g., wagging your tail, flapping your wings, purring) to make it feel real."""


class OpenAIService:
    """Handles OpenAI API calls for transcription, chat with skills, and TTS."""

    def __init__(self):
        self._client = None

    @property
    def client(self) -> AsyncOpenAI:
        if self._client is None:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                logger.warning("OPENAI_API_KEY not set.")
            self._client = AsyncOpenAI(api_key=api_key)
        return self._client

    async def transcribe(self, audio_file_path: str) -> str:
        try:
            t0 = time.time()
            logger.info(f"Transcribing: {audio_file_path}")
            with open(audio_file_path, "rb") as audio_file:
                response = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en",
                )
            logger.info(f"Transcription ({time.time()-t0:.1f}s): {response.text}")
            return response.text
        except Exception as e:
            logger.error(f"Whisper failed: {e}", exc_info=True)
            raise

    async def generate_response(
        self,
        user_text: str,
        conversation_history: Optional[list] = None,
        character_context: Optional[dict] = None,
        tools: Optional[List[dict]] = None,
        skill_executor=None,
    ) -> str:
        """
        Generate AI response with optional tool/skill calling.

        Args:
            user_text: What the child said
            conversation_history: Previous messages
            character_context: Character info for system prompt
            tools: List of OpenAI tool definitions from skill registry
            skill_executor: Async callable(name, args) -> str that executes a skill
        """
        try:
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
                "max_tokens": 150,
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
                # Add assistant's tool call message
                messages.append(message)

                # Execute each tool call
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
                    max_tokens=150,
                    temperature=0.8,
                )
                ai_text = final_response.choices[0].message.content
            else:
                ai_text = message.content

            logger.info(f"AI response: {ai_text}")
            return ai_text

        except Exception as e:
            logger.error(f"GPT failed: {e}", exc_info=True)
            raise

    async def generate_response_streaming(
        self,
        user_text: str,
        conversation_history: Optional[list] = None,
        character_context: Optional[dict] = None,
        tools: Optional[List[dict]] = None,
        skill_executor=None,
    ) -> AsyncGenerator[str, None]:
        """Stream GPT response, yielding sentence chunks as they complete."""
        try:
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

            request_kwargs = {
                "model": "gpt-4o-mini",
                "messages": messages,
                "max_tokens": 150,
                "temperature": 0.8,
                "stream": True,
            }

            # If tools are present, do a non-streaming call first to handle tool calls
            if tools:
                request_kwargs_nostream = {**request_kwargs, "stream": False, "tools": tools, "tool_choice": "auto"}
                response = await self.client.chat.completions.create(**request_kwargs_nostream)
                message = response.choices[0].message

                if message.tool_calls and skill_executor:
                    messages.append(message)
                    for tool_call in message.tool_calls:
                        fn_name = tool_call.function.name
                        fn_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
                        logger.info(f"Executing skill: {fn_name}({fn_args})")
                        result = await skill_executor(fn_name, fn_args)
                        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

                    # Stream the final response after tool execution
                    request_kwargs["messages"] = messages
                elif message.content:
                    # No tool calls — just yield the whole response
                    yield message.content
                    return

            # Stream response, yield on sentence boundaries
            logger.info(f"Streaming response for: {user_text}")
            stream = await self.client.chat.completions.create(**request_kwargs)
            buffer = ""
            sentence_enders = {'.', '!', '?'}

            async for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    buffer += delta.content
                    # Yield on sentence boundaries
                    while buffer:
                        end_idx = -1
                        for i, ch in enumerate(buffer):
                            if ch in sentence_enders:
                                end_idx = i
                                break
                        if end_idx >= 0:
                            sentence = buffer[:end_idx + 1].strip()
                            buffer = buffer[end_idx + 1:]
                            if sentence:
                                yield sentence
                        else:
                            break

            # Yield any remaining text
            if buffer.strip():
                yield buffer.strip()

        except Exception as e:
            logger.error(f"GPT streaming failed: {e}", exc_info=True)
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
