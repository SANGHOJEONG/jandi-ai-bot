import os
import time
from google import genai
from google.genai import errors
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 마크다운 매뉴얼 텍스트 로딩
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANUAL_PATH = os.path.join(BASE_DIR, "docs", "manual.md")

try:
    with open(MANUAL_PATH, "r", encoding="utf-8") as f:
        manual_content = f.read()
    print(f"매뉴얼 로딩 완료 ({len(manual_content)}자)")
except Exception as e:
    manual_content = "매뉴얼 파일을 불러올 수 없습니다."
    print(f"매뉴얼 로딩 오류: {e}")

def ask_claude(question: str) -> str:
    prompt = f"""당신은 백화점 직원을 위한 업무 매뉴얼 Q&A 어시스턴트입니다.

[규칙]
1. 반드시 제공된 매뉴얼 내용만 참고하여 답변하세요.
2. 매뉴얼에 없는 내용은 절대 답변하지 말고 "관련 내용을 매뉴얼에서 찾을 수 없습니다."라고 답하세요.
3. 외부 지식이나 일반 상식을 사용하지 마세요.
4. 답변은 친절하고 명확하게 작성하세요.
5. 출처가 되는 매뉴얼 항목을 함께 알려주세요.
6. 답변은 반드시 한국어로 작성하세요.

[매뉴얼 내용]
{manual_content}

[질문]
{question}"""

    models_to_try = [
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash",
        "gemini-flash-latest"
    ]

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text
        except errors.APIError as e:
            print(f"{model_name} 실패: {e}")
            time.sleep(2)
            continue
        except Exception as e:
            print(f"{model_name} 알 수 없는 오류: {e}")
            time.sleep(2)
            continue

    return "현재 AI 서버에 트래픽이 몰려 답변을 생성할 수 없습니다. 잠시 후 다시 질문해 주세요."