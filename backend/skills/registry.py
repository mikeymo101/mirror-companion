"""Skill registry — auto-discovers and manages all available skills."""

import os
import importlib
import logging
from typing import Dict, List, Optional

from skills.base import Skill

logger = logging.getLogger("mirror-companion.skills")


class SkillRegistry:
    """Discovers, registers, and manages skills."""

    def __init__(self):
        self._skills: Dict[str, Skill] = {}

    def register(self, skill: Skill):
        """Register a skill instance."""
        self._skills[skill.name] = skill
        logger.info(f"Registered skill: {skill.name}")

    def get(self, name: str) -> Optional[Skill]:
        """Get a skill by name."""
        return self._skills.get(name)

    def get_all_tool_definitions(self) -> List[dict]:
        """Get OpenAI tool definitions for all registered skills."""
        return [skill.get_tool_definition() for skill in self._skills.values()]

    def list_skills(self) -> List[str]:
        """List all registered skill names."""
        return list(self._skills.keys())

    def auto_discover(self):
        """Auto-discover and register all skill modules in the skills/ directory.
        Any .py file in skills/ that has a `create_skill()` function will be loaded."""
        skills_dir = os.path.dirname(__file__)
        for filename in sorted(os.listdir(skills_dir)):
            if filename.startswith("_") or not filename.endswith(".py"):
                continue
            if filename in ("base.py", "registry.py"):
                continue
            module_name = f"skills.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "create_skill"):
                    skill = module.create_skill()
                    self.register(skill)
            except Exception as e:
                logger.error(f"Failed to load skill {module_name}: {e}", exc_info=True)


# Global singleton
skill_registry = SkillRegistry()
