from openai import OpenAI
from app.core.config import OPENAI_API_KEY, OPENAI_BASE_URL
from typing import Dict

from app.models.memory import Memory
from app.core.database import SessionLocal

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

# # 多用户独立会话存储
# session_histories: Dict[str, list] = {}

def chat_with_ai(message: str, session_id: str):

    db = SessionLocal()

    # 查询历史消息
    histories = db.query(Memory)\
        .filter(Memory.session_id == session_id)\
        .all()

    # system prompt
    messages = [
        {
            "role": "system",
            "content": """
            你是章鱼哥，一个聪明、礼貌又幽默的 AI 助手。

            你必须记住用户在当前会话中提供的信息。

            包括：
            - 名字
            - 昵称
            - 爱好
            - 身份

            当用户询问历史内容时，
            你应该基于历史消息回答。
            """
        }
    ]

    # 添加历史消息
    for history in histories:
        messages.append({
            "role": history.role,
            "content": history.content
        })

    # 当前用户消息
    messages.append({
        "role": "user",
        "content": message
    })

    # 存储用户消息
    user_memory = Memory(
        session_id=session_id,
        role="user",
        content=message
    )
    db.add(user_memory)

    # 调用AI
    response = client.chat.completions.create(
        model="qwen-max",
        messages=messages
    )
    ai_message = response.choices[0].message.content

    # 存储AI消息
    ai_memory = Memory( 
        session_id=session_id,
        role="assistant",
        content=ai_message
    )
    db.add(ai_memory)
    db.commit()
    db.close()

    return ai_message