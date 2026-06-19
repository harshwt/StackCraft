from agent import Agent

with open("prompts/design.txt", "r", encoding="utf-8") as file:
    design_prompt = file.read()

design_agent = Agent(
    "design_agent",
    design_prompt
)