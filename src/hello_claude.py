from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "In one sentence, what is a non-compete clause?"}],
)

print(response.content[0].text)
print("Tokens in:", response.usage.input_tokens, "| out:", response.usage.output_tokens)