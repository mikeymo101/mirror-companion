"""Jokes skill — tells age-appropriate jokes."""

import random

from skills.base import Skill


class JokesSkill(Skill):
    name = "tell_joke"
    description = "Tell a funny, age-appropriate joke"

    JOKES = [
        ("Why did the teddy bear say no to dessert?", "Because she was already stuffed!"),
        ("What do you call a sleeping dinosaur?", "A dino-snore!"),
        ("Why did the banana go to the doctor?", "Because it wasn't peeling well!"),
        ("What do you call a fish without eyes?", "A fsh!"),
        ("Why can't you give Elsa a balloon?", "Because she will let it go!"),
        ("What do you call a dog that does magic tricks?", "A Labracadabrador!"),
        ("Why did the cookie go to the hospital?", "Because it felt crummy!"),
        ("What do you call a bear with no teeth?", "A gummy bear!"),
        ("Why do bees have sticky hair?", "Because they use honeycombs!"),
        ("What did the ocean say to the beach?", "Nothing, it just waved!"),
        ("What do you call a cow with no legs?", "Ground beef!"),
        ("Why did the golfer bring two pairs of pants?", "In case he got a hole in one!"),
        ("What animal is always at a baseball game?", "A bat!"),
        ("Why couldn't the pony sing?", "Because she was a little hoarse!"),
        ("What do you call cheese that isn't yours?", "Nacho cheese!"),
        ("Why do ducks have tail feathers?", "To cover their butt quacks!"),
        ("What do elves learn in school?", "The elf-abet!"),
        ("What did the big flower say to the little flower?", "Hi there, bud!"),
        ("Why was 6 afraid of 7?", "Because 7 ate 9!"),
        ("What do you call a pig that does karate?", "A pork chop!"),
    ]

    def get_tool_definition(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": (
                    "Tell a funny joke that's appropriate for young children. "
                    "Use this when the child asks for a joke, wants to laugh, "
                    "or says they're bored."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        }

    async def execute(self, **kwargs) -> str:
        setup, punchline = random.choice(self.JOKES)
        return f"Here's a joke! {setup} ... {punchline}"


def create_skill():
    return JokesSkill()
