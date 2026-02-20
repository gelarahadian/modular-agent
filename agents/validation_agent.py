from langchain_ollama import ChatOllama
from schemas.models import ValidationOutput
from utils.json_parser import extract_json

llm = ChatOllama(
    model="gemma3:4b",
    temperature=0
)

def validation_agent(task: str, result: str) -> ValidationOutput:
    prompt = f"""
    You are a validation agent.

    Review the result for correctness and logical consistency.
    Approve only if reasoning is sound.

    Respond ONLY in JSON:
    {{
        "approved": true or false,
        "feedback": "..."
    }}

    Task: {task}
    Result: {result}
    """

    response = llm.invoke(prompt)

    parsed = extract_json(response.content)

    return ValidationOutput(**parsed)
