from agent import Agent

with open("prompts/intent.txt", "r", encoding='utf-8') as file:
    intent_prompt = file.read()

intent_agent = Agent(
    "intent_agent",
    intent_prompt
)

