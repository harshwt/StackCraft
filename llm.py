import os
from dotenv import load_dotenv
from groq import Groq

# AutoGen client support for future agent extensions
try:
    from autogen_ext.models.openai import OpenAIChatCompletionClient
except ImportError:
    OpenAIChatCompletionClient = None

load_dotenv()

DEFAULT_MODELS = [
    os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
]

_client = None

def get_groq_client() -> Groq:
    global _client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")
    if _client is None:
        _client = Groq(api_key=api_key)
    return _client

def call_llm(system_prompt: str, user_message: str, model: str | None = None) -> str:
    """Call LLM synchronously using Groq with automatic fallback."""
    client = get_groq_client()
    models_to_try = [model] if model else DEFAULT_MODELS

    last_err = None
    for m in models_to_try:
        if not m:
            continue
        try:
            response = client.chat.completions.create(
                model=m,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.2,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
        except Exception as e:
            last_err = e
            # Try next model if model not found
            continue

    raise RuntimeError(f"All LLM models failed. Last error: {last_err}")

def model_client():
    """Create an AutoGen framework model client using Groq's OpenAI-compatible API."""
    if OpenAIChatCompletionClient is None:
        raise ImportError("autogen_ext is required for model_client().")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    return OpenAIChatCompletionClient(
        model=model,
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
            "structured_output": False,
        },
        temperature=0.3,
    )
