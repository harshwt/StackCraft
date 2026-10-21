from llm import call_llm

REPAIR_SYSTEM_PROMPT = """You are a Schema Repair Agent.
Your task is to fix malformed or incomplete application schema JSON.

Ensure the output is strictly valid JSON containing all 4 required sections as objects:
{
  "ui": {
    "pages": []
  },
  "api": {
    "endpoints": [
      {
        "path": "/api/...",
        "method": "GET"
      }
    ]
  },
  "database": {
    "tables": []
  },
  "auth": {
    "type": "JWT"
  }
}

Return ONLY valid JSON without any markdown formatting or explanations.
"""

def repair_schema(invalid_schema: str, error_message: str, context: str = "") -> str:
    """Attempt to repair an invalid schema using the LLM."""
    prompt = f"""The following application schema failed validation with error: "{error_message}".

Context / Requirements:
{context}

Invalid Schema:
{invalid_schema}

Fix the schema so that it is valid JSON with valid 'ui', 'api', 'database', and 'auth' objects.
Return ONLY valid JSON.
"""
    try:
        repaired = call_llm(REPAIR_SYSTEM_PROMPT, prompt)
        return repaired.strip()
    except Exception as e:
        print(f"Schema repair attempt failed: {e}")
        return invalid_schema
