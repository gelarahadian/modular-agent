from langchain_ollama import ChatOllama
from schemas.models import IntakeOutput
from utils.json_parser import extract_json

llm = ChatOllama(
    model="gemma3:4b",
    temperature=0
)

def intake_agent(user_input: str):
    prompt = f"""
    You are a task intake classifier.
    Classify the task into one of these categories:
    - analysis
    - generation
    - validation
    - unknown

    Task: {user_input}

    Respond in this JSON format:
    {{
        "category": "...",
        "reasoning": "..."
    }}
    """

    response = llm.invoke(prompt)
    parsed = extract_json(response.content)
    return IntakeOutput(**parsed)
