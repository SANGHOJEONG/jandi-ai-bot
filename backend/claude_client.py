import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def ask_claude(question: str) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="당신은 사내 업무를 지원하는 AI 어시스턴트입니다. 친절하고 명확하게 답변해주세요.",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return message.content[0].text