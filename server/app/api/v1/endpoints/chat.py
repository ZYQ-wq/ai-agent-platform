from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import deps
from app.schemas.chat import ChatMessage
from app.services import chat_service

router = APIRouter()

# MVP 阶段：暂时固定用户ID，后续接入真实的 Token 解析
def get_current_user_id():
    return 1 

@router.post("/send")
def send_message(msg: ChatMessage, db: Session = Depends(deps.get_db)):
    user_id = get_current_user_id()
    
    # 1. 保存用户输入
    chat_service.save_message(db, user_id, "user", msg.content)
    
    # 2. 模拟 AI 回复 (MVP 硬编码)
    ai_response = "收到你的消息：" + msg.content
    
    # 3. 保存 AI 回复
    chat_service.save_message(db, user_id, "assistant", ai_response)
    
    return {"response": ai_response}

@router.get("/history")
def get_history(db: Session = Depends(deps.get_db)):
    user_id = get_current_user_id()
    # 倒序取出后，在代码中反转，保证时间正序
    history = chat_service.get_history(db, user_id)
    return list(reversed(history))