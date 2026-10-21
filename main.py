from pipeline.intent import intent_agent
from pipeline.design import design_agent
from pipeline.schema import schema_agent
from validator import validate_schema
from codegen import generate_fastapi_code
from repair import repair_schema

def run_pipeline(user_prompt: str) -> dict:
    # Stage 1: Intent Extraction
    intent = intent_agent.run(user_prompt)

    # Stage 2: Architecture Design (with requirement context)
    design_input = f"""Original User Requirement:
{user_prompt}

Extracted Intent:
{intent}"""
    design = design_agent.run(design_input)

    # Stage 3: Schema Generation (with full intent + design context)
    schema_input = f"""Original User Requirement:
{user_prompt}

Extracted Intent:
{intent}

System Architecture Design:
{design}"""
    schema = schema_agent.run(schema_input)

    # Stage 4: Validation & Self-Healing Repair
    valid, message = validate_schema(schema)
    repaired = False

    if not valid:
        print(f"[Validator] Validation failed: {message}. Attempting auto-repair...")
        candidate_schema = repair_schema(schema, message, schema_input)
        repaired_valid, repaired_message = validate_schema(candidate_schema)
        if repaired_valid:
            schema = candidate_schema
            valid = True
            message = "Schema repaired successfully"
            repaired = True
            print("[Validator] Schema successfully repaired!")
        else:
            print(f"[Validator] Auto-repair was unsuccessful: {repaired_message}")

    # Stage 5: Code Generation
    get_code = ""
    if valid:
        get_code = generate_fastapi_code(schema)

    return {
        "intent": intent,
        "design": design,
        "schema": schema,
        "valid": valid,
        "message": message,
        "repaired": repaired,
        "generated_code": get_code
    }

def main():
    user_prompt = input("Describe your application:\n")
    if not user_prompt.strip():
        print("Empty prompt provided. Exiting.")
        return

    result = run_pipeline(user_prompt)

    print("\n" + "=" * 50)
    print("STATUS:", "VALID" if result["valid"] else "INVALID")
    print("MESSAGE:", result["message"])
    print("=" * 50)
    print("\n--- SCHEMA ---")
    print(result["schema"])

    if result["generated_code"]:
        print("\n--- GENERATED FASTAPI CODE ---")
        print(result["generated_code"])

if __name__ == "__main__":
    main()
