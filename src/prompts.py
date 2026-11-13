from src.config import RISKS


def build_system_prompt():
    risk_lines = "\n".join(
        f'- "{key}": {risk["definition"]}' for key, risk in RISKS.items()
    )
    return f"""You are a careful contract reviewer. You will be given the full text of a commercial contract.

For each of the six risk types below, decide whether the contract contains it.

Risk types (key: definition):
{risk_lines}

Rules:
1. Base every answer only on the contract text.
2. "quotes" must be copied word for word from the contract. Never paraphrase.
3. If a risk is not present, set "present" to false and "quotes" to [].
4. Keep each "explanation" to one sentence.

Respond with only a JSON object, no other text, in exactly this shape:
{{
  "uncapped_liability": {{"present": true, "quotes": ["..."], "explanation": "..."}},
  ...one entry for each of the six keys above...
}}"""


def build_user_message(contract_text):
    return f"Here is the contract to review:\n\n{contract_text}"
