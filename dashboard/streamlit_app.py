import streamlit as st
import os
from google import genai
from google.genai import errors
import time

# Gemini 클라이언트 설정
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 매뉴얼 로딩
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANUAL_PATH = os.path.join(BASE_DIR, "docs", "manual.md")

try:
    with open(MANUAL_PATH, "r", encoding="utf-8") as f:
        manual_content = f.read()
except Exception as e:
    manual_content = "매뉴얼 파일을 불러올 수 없습니다."

def ask_gemini(question: str) -> str:
    prompt = f"""당신은 롯데백화점몰 파트너사 직원을 위한 업무 매뉴얼 Q&A 어시스턴트입니다.

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
        except Exception as e:
            print(f"{model_name} 실패: {e}")
            time.sleep(2)
            continue

    return "현재 AI 서버에 트래픽이 몰려 답변을 생성할 수 없습니다. 잠시 후 다시 질문해 주세요."

# 페이지 설정
st.set_page_config(
    page_title="롯데백화점몰 업무 매뉴얼 Q&A",
    page_icon="📚",
    layout="centered"
)

# 헤더
st.title("📚 롯데백화점몰 업무 매뉴얼 Q&A")
st.markdown("궁금한 업무 내용을 질문하시면 매뉴얼을 기반으로 답변해드립니다.")
st.divider()

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 표시
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# 질문 입력
if prompt := st.chat_input("질문을 입력해주세요..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("매뉴얼에서 답변을 찾고 있습니다..."):
            answer = ask_gemini(prompt)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})