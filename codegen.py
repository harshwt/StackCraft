import json

def generate_fastapi_code(schema):

    print("SCHEMA RECEIVED:")
    print(repr(schema))

    if not schema:
        return "# No schema generated"

    schema = schema.strip()

    if schema.startswith("```json"):
        schema = schema.replace("```json", "", 1)

    if schema.endswith("```"):
        schema = schema[:-3]

    try:
        schema = json.loads(schema)

    except Exception as e:

        return f"# Failed to parse schema\n# {e}"

    code = """
from fastapi import FastAPI

app = FastAPI()
"""

    endpoints = schema.get("api", {}).get(
        "endpoints",
        []
    )

    for endpoint in endpoints:

        code += f"""

@app.get("{endpoint}")
def {endpoint.replace('/', '_').strip('_')}():
    return {{"message": "ok"}}
"""

    return code