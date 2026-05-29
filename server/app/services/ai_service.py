from openai import OpenAI

from app.core.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL
)

from app.models.memory import Memory
from app.models.user import User
from app.models.agent import Agent

from app.core.database import SessionLocal


client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)


def chat_with_agent(
    message,
    user_email,
    agent_id
):

    db = SessionLocal()

    try:

        # 查询用户
        user = db.query(User).filter(
            User.email == user_email
        ).first()

        if not user:

            raise Exception("用户不存在")

        # 查询Agent
        agent = db.query(Agent).filter(
            Agent.id == agent_id,
            Agent.user_id == user.id
        ).first()

        if not agent:

            raise Exception("Agent不存在")

        # 查询历史记忆
        histories = db.query(Memory).filter(
            Memory.user_id == user.id,
            Memory.agent_id == agent.id
        ).all()

        # system prompt
        messages = [
            {
                "role": "system",
                "content": agent.system_prompt
            }
        ]

        # 历史消息
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

        # 保存用户消息
        user_memory = Memory(
            user_id=user.id,
            agent_id=agent.id,
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

        # 保存AI消息
        ai_memory = Memory(
            user_id=user.id,
            agent_id=agent.id,
            role="assistant",
            content=ai_message
        )

        db.add(ai_memory)

        db.commit()

        return ai_message

    finally:

        db.close()
