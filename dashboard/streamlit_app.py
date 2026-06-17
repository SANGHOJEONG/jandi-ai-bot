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
    prompt = f"""당신은 롯데백화점몰 파트너사 직원을 위한 업무 어시스턴트입니다.

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
            time.sleep(2)
            continue

    return "현재 AI 서버에 트래픽이 몰려 답변을 생성할 수 없습니다. 잠시 후 다시 질문해 주세요."

# 페이지 설정
st.set_page_config(
    page_title="롯데백화점몰 파트너 어시스턴트",
    page_icon="🛍️",
    layout="centered"
)

# CSS 스타일
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background-color: #fff9f9;
    }
    
    /* 헤더 배너 */
    .header-banner {
        background: linear-gradient(135deg, #c8102e 0%, #8b0000 100%);
        padding: 40px 30px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(200, 16, 46, 0.3);
    }
    .header-banner h1 {
        color: white;
        font-size: 2rem;
        font-weight: 800;
        margin: 0 0 8px 0;
        letter-spacing: -0.5px;
    }
    .header-banner p {
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
        margin: 0;
    }
    .header-banner .emoji {
        font-size: 2.5rem;
        margin-bottom: 12px;
        display: block;
    }

    /* 안내 카드 */
    .info-card {
        background: white;
        border-left: 4px solid #c8102e;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        font-size: 0.9rem;
        color: #555;
    }

    /* 예시 질문 */
    .example-title {
        font-size: 0.85rem;
        color: #999;
        margin-bottom: 8px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .example-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 24px;
    }
    .chip {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 0.85rem;
        color: #c8102e;
        cursor: pointer;
    }

    /* 푸터 */
    .footer {
        text-align: center;
        color: #aaa;
        font-size: 0.8rem;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #eee;
    }
    .footer a {
        color: #c8102e;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# 헤더 배너
st.markdown("""
<div class="header-banner">
    <span class="emoji">🛍️</span>
    <h1>롯데백화점몰 파트너 어시스턴트</h1>
    <p>궁금한 건 뭐든지 물어보세요! 매뉴얼을 샅샅이 뒤져 바로 답해드립니다 😊</p>
</div>
""", unsafe_allow_html=True)

# 안내 카드
st.markdown("""
<div class="info-card">
    💡 <strong>이런 것들을 물어보실 수 있어요</strong><br>
    상품 등록 방법 · 정산 절차 · 반품/교환 처리 · 프로모션 참여 방법 · 시스템 사용법
</div>
""", unsafe_allow_html=True)

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 표시
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🛍️"):
            st.markdown(message["content"])

# 대화 초기화 버튼
if st.session_state.messages:
    if st.button("🔄 대화 초기화", type="secondary"):
        st.session_state.messages = []
        st.rerun()

# 질문 입력
if prompt := st.chat_input("무엇이든 물어보세요..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🛍️"):
        with st.spinner("매뉴얼을 확인하고 있습니다..."):
            answer = ask_gemini(prompt)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

# 푸터
st.markdown("""
<div class="footer">
    <a href="https://www.ellotte.com" target="_blank">롯데백화점몰 바로가기</a> · 
    본 서비스는 파트너사 전용입니다
</div>
""", unsafe_allow_html=True)