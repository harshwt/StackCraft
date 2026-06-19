from pipeline.intent import intent_agent
from pipeline.design import design_agent
from pipeline.schema import schema_agent
from validator import validate_schema
from codegen import generate_fastapi_code

def run_pipeline(user_prompt):

    intent = intent_agent.run(user_prompt)

    design = design_agent.run(intent)

    schema = schema_agent.run(design)

    valid, message = validate_schema(schema)
    get_code = ""

    if valid:
        get_code = generate_fastapi_code(schema)


    return {
        "intent": intent,
        "design": design,
        "schema": schema,
        "valid": valid,
        "message": message,
        "generated_code": get_code
    }


def main():

    user_prompt = input(
        "Describe your application:\n"
    )

    result = run_pipeline(user_prompt)

    print(result["schema"])


if __name__ == "__main__":
    main()

