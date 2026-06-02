from fastapi import HTTPException

from app.models.agent import Agent
from app.models.user import User

from app.models.memory import Memory
from app.models.memory_summary import MemorySummary

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

def update_agent_service(
    agent_id,
    req,
    user_email
):

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

        agent = db.query(Agent).filter(
            Agent.id == agent_id,
            Agent.user_id == user.id
        ).first()

        if not agent:

            raise HTTPException(
                status_code=404,
                detail="Agent不存在"
            )

        agent.name = req.name
        agent.description = req.description
        agent.system_prompt = req.system_prompt

        db.commit()

        db.refresh(agent)

        return agent

    finally:

        db.close()

def get_agent_service(agent_id, user_email):
    """获取单个Agent"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(404, "用户不存在")

        agent = db.query(Agent).filter(
            Agent.id == agent_id,
            Agent.user_id == user.id
        ).first()

        if not agent:
            raise HTTPException(404, "Agent不存在")

        return agent
    finally:
        db.close()

# def delete_agent_service(agent_id, user_email):
#     """删除Agent"""
#     db = SessionLocal()
#     try:
#         user = db.query(User).filter(User.email == user_email).first()
#         if not user:
#             raise HTTPException(404, "用户不存在")

#         agent = db.query(Agent).filter(
#             Agent.id == agent_id,
#             Agent.user_id == user.id
#         ).first()

#         if not agent:
#             raise HTTPException(404, "Agent不存在")

#         db.delete(agent)
#         db.commit()
#         return {"detail": "删除成功"}
#     finally:
#         db.close()
def delete_agent_service(agent_id: int, user_email: str):
    db = SessionLocal()
    try:
        # 查询用户
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )

        # 查询Agent
        agent = db.query(Agent).filter(
            Agent.id == agent_id,
            Agent.user_id == user.id
        ).first()

        if not agent:
            raise HTTPException(
                status_code=404,
                detail="Agent不存在"
            )

        # 先删除Memory表中与该Agent相关的记录
        db.query(Memory).filter(
            Memory.agent_id == agent.id
        ).delete(synchronize_session=False)

        # 删除MemorySummary表中与该Agent相关的记录
        db.query(MemorySummary).filter(
            MemorySummary.agent_id == agent.id
        ).delete(synchronize_session=False)

        # 删除Agent本身
        db.delete(agent)

        db.commit()

        return {"message": "删除成功"}

    finally:
        db.close()