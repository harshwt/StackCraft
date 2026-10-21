import asyncio
import concurrent.futures
from autogen_agentchat.agents import AssistantAgent
from llm import model_client

class Agent:
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.client = model_client()

        self.agent = AssistantAgent(
            name=name,
            model_client=self.client,
            system_message=system_prompt,
        )

    async def run_async(self, message: str) -> str:
        """Run the AutoGen assistant agent asynchronously with retry on transient rate limits."""
        print(f"\n[{self.name}] Running...")
        max_attempts = 4
        for attempt in range(1, max_attempts + 1):
            try:
                response = await self.agent.run(task=message)
                content = response.messages[-1].content
                return content if isinstance(content, str) else str(content)
            except Exception as e:
                err_str = str(e).lower()
                if ("rate_limit" in err_str or "429" in err_str) and attempt < max_attempts:
                    wait_time = attempt * 3
                    print(f"[{self.name}] Rate limit (429) encountered. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                else:
                    raise e

    def run(self, message: str) -> str:
        """Run the agent synchronously, handling any active asyncio event loops safely."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                return executor.submit(asyncio.run, self.run_async(message)).result()
        else:
            return asyncio.run(self.run_async(message))