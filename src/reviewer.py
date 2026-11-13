import json

import anthropic
from dotenv import load_dotenv

from src.prompts import build_system_prompt, build_user_message

load_dotenv()
client = anthropic.Anthropic(max_retries=8)


def review_contract(contract_text, model="claude-haiku-5-5"):
    response = client.messages.create(
        model=model,
        max_tokens=4000,
        system=build_system_prompt(),
        messages=[{"role": "user", "content": build_user_message(contract_text)}],
    )
    text = "".join(block.text for block in response.content if block.type == "text")
    result = json.loads(text[text.find("{"): text.rfind("}") + 1])
    return result, response.usage


