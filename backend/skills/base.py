"""Base class for all Mirror Companion skills."""

import logging
from abc import ABC, abstractmethod


class Skill(ABC):
    """Base class that all skills must inherit from."""

    # Subclasses must define these
    name: str = ""           # e.g. "weather"
    description: str = ""    # e.g. "Get current weather information"

    def __init__(self):
        self.logger = logging.getLogger(f"mirror-companion.skill.{self.name}")

    @abstractmethod
    def get_tool_definition(self) -> dict:
        """Return the OpenAI function/tool definition for this skill.
        Format: {"type": "function", "function": {"name": ..., "description": ..., "parameters": ...}}
        """
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """Execute the skill with the given parameters. Returns a text result that gets fed back to GPT."""
        pass
