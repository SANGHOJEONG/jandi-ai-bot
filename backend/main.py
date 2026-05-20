from fastapi import FastAPI, Request
from backend.claude_client import ask_claude
from backend.jandi_client import send_to_jandi

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/jandi")
async def jandi_webhook(request: Request):
    data = await request.json()
    
    # 메시지 추출
    text = data.get("text", "")
    
    # 키워드 제거 (/AI 또는 @AI)
    question = text.replace("/AI", "").replace("@AI", "").strip()
    
    if not question:
        return {"status": "no question"}
    
    # Claude에게 질문
    answer = ask_claude(question)
    
    # JANDI로 답변 전송
    send_to_jandi(answer)
    
    return {"status": "ok"}