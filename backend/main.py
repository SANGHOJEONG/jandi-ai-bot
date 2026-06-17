import threading
import time
import requests
from datetime import datetime
import pytz
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
    
    # 키워드 제거
    question = text.replace("/이커머스매뉴얼", "").replace("/AI", "").replace("@AI", "").strip()
    
    if not question:
        return {"status": "no question"}
    
    # Gemini에게 질문
    answer = ask_claude(question)
    
    # JANDI로 답변 전송
    send_to_jandi(answer)
    
    return {"status": "ok"}

def self_ping():
    """업무시간(08:40 ~ 19:00)에만 10분마다 자기 자신에게 핑 전송"""
    KST = pytz.timezone("Asia/Seoul")
    
    while True:
        now = datetime.now(KST)
        current_time = now.time()
        
        start_time = now.replace(hour=8, minute=40, second=0).time()
        end_time = now.replace(hour=19, minute=0, second=0).time()
        
        if start_time <= current_time <= end_time:
            try:
                requests.get("https://jandi-ai-bot.onrender.com", timeout=10)
                print(f"[{now.strftime('%H:%M')}] 핑 전송 완료 ✅")
            except Exception as e:
                print(f"[{now.strftime('%H:%M')}] 핑 실패: {e}")
        else:
            print(f"[{now.strftime('%H:%M')}] 업무시간 외 — 핑 생략")
        
        time.sleep(600)  # 10분 대기

# 서버 시작 시 백그라운드에서 핑 스레드 실행
ping_thread = threading.Thread(target=self_ping, daemon=True)
ping_thread.start()