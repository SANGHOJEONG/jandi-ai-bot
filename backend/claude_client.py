import os
from google import genai
from dotenv import load_dotenv
from backend.ppt_reader import extract_text_from_ppt

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# PPT 매뉴얼 텍스트 추출
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PPT_PATH = os.path.join(BASE_DIR, "docs", "manual1.pptx")

try:
    manual_content = extract_text_from_ppt(PPT_PATH)
except Exception as e:
    manual_content = "매뉴얼 파일을 불러올 수 없습니다."
    print(f"PPT 로딩 오류: {e}")

def ask_claude(question: str) -> str:
    prompt = f"""당신은 백화점 직원을 위한 업무 매뉴얼 Q&A 어시스턴트입니다.

[규칙]
1. 반드시 제공된 매뉴얼 내용만 참고하여 답변하세요.
2. 매뉴얼에 없는 내용은 절대 답변하지 말고 "관련 내용을 매뉴얼에서 찾을 수 없습니다."라고 답하세요.
3. 외부 지식이나 일반 상식을 사용하지 마세요.
4. 답변은 친절하고 명확하게 작성하세요.
5. 출처가 되는 매뉴얼 항목을 함께 알려주세요.

[매뉴얼 내용]
{manual_content}

[질문]
{question}"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=prompt
    )
    return response.text