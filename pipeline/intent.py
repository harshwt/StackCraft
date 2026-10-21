from pathlib import Path
from agent import Agent

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

with open(PROMPTS_DIR / "intent.txt", "r", encoding="utf-8") as file:
    intent_prompt = file.read()

intent_agent = Agent(
    "intent_agent",
    intent_prompt
)
