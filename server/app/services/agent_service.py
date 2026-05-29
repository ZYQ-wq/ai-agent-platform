from fastapi import HTTPException

from app.models.agent import Agent
from app.models.user import User

from app.core.database import SessionLocal


# 创建Agent
def create_agent_service(
    user_email,
    name,
    description,
    system_prompt
):

    db = SessionLocal()

    try:

        # 查询用户
        user = db.query(User).filter(
            User.email == user_email
        ).first()

        if not user:

            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )

        # 创建Agent
        agent = Agent(
            user_id=user.id,
            name=name,
            description=description,
            system_prompt=system_prompt
        )

        db.add(agent)

        db.commit()

        db.refresh(agent)

        return agent

    finally:

        db.close()


# 获取我的Agent列表
def get_agents_service(user_email):

    db = SessionLocal()

    try:

        user = db.query(User).filter(
            User.email == user_email
        ).first()

        if not user:

            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )

        agents = db.query(Agent).filter(
            Agent.user_id == user.id
        ).all()

        return agents

    finally:

        db.close()

