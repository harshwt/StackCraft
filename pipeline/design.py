from pathlib import Path
from agent import Agent

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

with open(PROMPTS_DIR / "design.txt", "r", encoding="utf-8") as file:
    design_prompt = file.read()

design_agent = Agent(
    "design_agent",
    design_prompt
)