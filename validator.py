import json

def validate_schema(schema_txt):

    schema_txt = schema_txt.strip()

    if schema_txt.startswith("```json"):
        schema_txt = schema_txt.replace("```json", "", 1)

    if schema_txt.endswith("```"):
        schema_txt = schema_txt[:-3]

    try:
        schema = json.loads(schema_txt)
    except Exception as e:
        return False, f"Invalid JSON: {e}"

    required_sections = [
        "ui",
        "api",
        "database",
        "auth"
    ]

    for section in required_sections:
        if section not in schema:
            return False, f"Missing section: {section}"

        if not isinstance(schema[section], dict):
            return False, f"{section} must be an object"

    return True, "Valid Response"