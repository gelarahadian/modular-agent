import json
import re


def extract_json(text: str):
    """
    Extract first valid JSON object from model response.
    """

    # Remove markdown code blocks if exist
    text = re.sub(r"```json|```", "", text)

    # Find first JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in response.")

    json_str = match.group(0)

    return json.loads(json_str)