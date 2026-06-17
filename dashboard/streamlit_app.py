import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.claude_client import ask_claude

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
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI 답변 생성
    with st.chat_message("assistant"):
        with st.spinner("매뉴얼에서 답변을 찾고 있습니다..."):
            answer = ask_claude(prompt)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})