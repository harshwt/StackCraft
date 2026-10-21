from pathlib import Path
from agent import Agent

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

with open(PROMPTS_DIR / "schema.txt", "r", encoding="utf-8") as file:
    schema_prompt = file.read()

schema_agent = Agent(
    "schema_agent",
    schema_prompt
)
