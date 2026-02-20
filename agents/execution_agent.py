from langchain_ollama import ChatOllama
from schemas.models import ExecutionOutput
from utils.json_parser import extract_json

llm = ChatOllama(
    model="gemma3:4b",
    temperature=0
)

def execution_agent(task: str) -> ExecutionOutput:
    prompt = f"""
    You are a rule-based execution agent.

    Solve the task with structured reasoning.
    Stay within logical constraints.
    Provide confidence score between 0 and 1.

    Respond ONLY in JSON:
    {{
        "result": "...",
        "reasoning": "...",
        "confidence": 0.0
    }}

    Task: {task}
    """

    response = llm.invoke(prompt)

    parsed = extract_json(response.content)

    return ExecutionOutput(**parsed)
