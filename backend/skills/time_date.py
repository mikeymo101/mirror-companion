"""Time and date skill — tells the child what time/day it is."""

from datetime import datetime

from skills.base import Skill


class TimeDateSkill(Skill):
    name = "get_time_and_date"
    description = "Get the current time, day of the week, and date"

    def get_tool_definition(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": (
                    "Get the current time, day of the week, and today's date. "
                    "Use this when the child asks what time it is, what day it is, "
                    "or what today's date is."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        }

    async def execute(self, **kwargs) -> str:
        now = datetime.now()
        hour = now.strftime("%I").lstrip("0")
        minute = now.strftime("%M")
        ampm = now.strftime("%p")
        day_name = now.strftime("%A")
        month_name = now.strftime("%B")
        day = now.day

        time_str = f"{hour}:{minute} {ampm}" if minute != "00" else f"{hour} {ampm}"
        return f"It's {time_str} on {day_name}, {month_name} {day}."


def create_skill():
    return TimeDateSkill()
