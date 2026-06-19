from llm import call_llm

class Agent:

    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt

    def run(self, message):

        print(f"\n[{self.name}] Running...")

        return call_llm(
            self.system_prompt,
            message
        )