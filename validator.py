import json
import re
from typing import Any, Dict, Optional, Tuple

def extract_json(raw_input: Any) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Extract and parse a JSON dictionary from a string or dictionary."""
    if isinstance(raw_input, dict):
        return raw_input, None

    if not isinstance(raw_input, str):
        return None, f"Expected string or dict, got {type(raw_input).__name__}"

    text = raw_input.strip()
    if not text:
        return None, "Empty response received"

    # Attempt 1: Direct JSON parsing
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed, None
    except Exception:
        pass

    # Attempt 2: Extract from markdown code fence ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if match:
        snippet = match.group(1).strip()
        try:
            parsed = json.loads(snippet)
            if isinstance(parsed, dict):
                return parsed, None
        except Exception:
            pass

    # Attempt 3: Slice between first '{' and last '}'
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace > first_brace:
        snippet = text[first_brace:last_brace + 1]
        try:
            parsed = json.loads(snippet)
            if isinstance(parsed, dict):
                return parsed, None
        except Exception as e:
            return None, f"Invalid JSON syntax: {e}"

    return None, "No valid JSON object found in response"

def validate_schema(schema_input: Any) -> Tuple[bool, str]:
    """Validate that the schema is valid JSON and contains required sections."""
    schema, error = extract_json(schema_input)
    if error:
        return False, error

    required_sections = [
        "ui",
        "api",
        "database",
        "auth"
    ]

    for section in required_sections:
        if section not in schema:
            return False, f"Missing required section: {section}"

        if not isinstance(schema[section], dict):
            return False, f"Section '{section}' must be a JSON object"

    return True, "Valid Response"