from agent import Agent

with open('prompts/schema.txt', 'r', encoding="utf-8") as file:
    schema_prompt = file.read()


schema_agent = Agent(
    "schema_agent",
    schema_prompt
)
