# from openai import OpenAI

# from app.core.config import (
#     OPENAI_API_KEY,
#     OPENAI_BASE_URL
# )

# from app.models.memory import Memory
# from app.models.user import User
# from app.models.agent import Agent
# from app.models.memory_summary import MemorySummary

# from app.services.embedding_service import get_embedding
# from app.services.memory_manager import MemoryManager

# import json

# from app.core.database import SessionLocal


# client = OpenAI(
#     api_key=OPENAI_API_KEY,
#     base_url=OPENAI_BASE_URL
# )


# def chat_with_agent(
#     message,
#     user_email,
#     agent_id
# ):

#     db = SessionLocal()

#     try:

#         # 查询用户
#         user = db.query(User).filter(
#             User.email == user_email
#         ).first()

#         if not user:

#             raise Exception("用户不存在")

#         # 查询Agent
#         agent = db.query(Agent).filter(
#             Agent.id == agent_id,
#             Agent.user_id == user.id
#         ).first()

#         if not agent:

#             raise Exception("Agent不存在")
        
#         # 初始化 MemoryManager 
#         memory_manager = MemoryManager()

#         # 获取短期历史
#         short_histories = memory_manager.get_recent( user.id, agent.id )

#         for h in short_histories:
#             h.embedding = json.loads(h.embedding) if h.embedding else None

#         # 获取长期摘要
#         long_summary = get_summary(user.id, agent.id, db)

#         # 3. 获取相关记忆（RAG） 
#         relevant_memories = memory_manager.search_relevant_memories( 
#             user.id, agent.id, message )

#         # system prompt + summary +短期历史
#         messages = []
#         if long_summary:
#             messages.append({"role": "system", "content": f"用户长期记忆摘要：{long_summary}"})

#         messages.append({"role": "system", "content": agent.system_prompt})

#         # RAG相关记忆 
#         if relevant_memories: 
#             memory_text = "\n".join([
#                 f"{m['role']}: {m['content']}" 
#                 for m in relevant_memories ]) 
            
#             messages.append({ "role": "system", "content": f"以下是与当前问题相关的历史记忆：\n{memory_text}" })

#         for h in short_histories:
#             # 【优化点】：先判断是不是字符串，防止重复解码报错
#             if isinstance(h.embedding, str):
#                 try:
#                     h.embedding = json.loads(h.embedding)
#                 except:
#                     h.embedding = None
#             # 如果已经是 list 或 None，就保持不动
        
#         for h in short_histories: 
#             messages.append({ "role": h["role"], "content": h["content"] })

#         # 当前用户消息
#         messages.append({"role": "user", "content": message})

#         # 调用AI
#         response = client.chat.completions.create(
#             model="qwen-max",
#             messages=messages
#         )
#         ai_message = response.choices[0].message.content

#         # 存储短期消息
#         memory_manager.add_message( user.id, agent.id, "user", message )

#         memory_manager.add_message( user.id, agent.id, "assistant", ai_message )

#         # 生成/更新长期摘要
#         # 简单策略：把所有短期历史和当前消息拼接后AI压缩成摘要
#         summary_input = "\n".join([h.content for h in short_histories] + [message, ai_message])
#         summary_response = client.chat.completions.create(
#             model="qwen-max",
#             messages=[{"role": "system", "content": "将以下内容压缩为长期摘要，只保留关键信息"} , {"role": "user", "content": summary_input}]
#         )
#         new_summary = summary_response.choices[0].message.content
#         update_summary(user.id, agent.id, new_summary, db)

#         return ai_message

#     finally:

#         db.close()


# def get_summary(user_id: int, agent_id: int, db):
#     """获取长期摘要"""
#     summary_obj = db.query(MemorySummary).filter(
#         MemorySummary.user_id == user_id,
#         MemorySummary.agent_id == agent_id
#     ).first()
#     if summary_obj:
#         return summary_obj.summary
#     return ""

# def update_summary(user_id: int, agent_id: int, new_summary: str, db):
#     """更新长期摘要"""
#     summary_obj = db.query(MemorySummary).filter(
#         MemorySummary.user_id == user_id,
#         MemorySummary.agent_id == agent_id
#     ).first()
#     if summary_obj:
#         summary_obj.summary = new_summary
#     else:
#         summary_obj = MemorySummary(
#             user_id=user_id,
#             agent_id=agent_id,
#             summary=new_summary
#         )
#         db.add(summary_obj)
#     db.commit()



from openai import OpenAI
import json

from app.core.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL
)

from app.models.memory import Memory
from app.models.user import User
from app.models.agent import Agent
from app.models.memory_summary import MemorySummary

from app.services.memory_manager import MemoryManager

from app.core.database import SessionLocal

# 关于工具调用
from app.tools.registry import tool_registry
from app.services.tool_call_service import execute_tool_call


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

        # 初始化 MemoryManager
        memory_manager = MemoryManager()

        # =========================
        # 1. 获取短期记忆
        # =========================
        short_histories = memory_manager.get_recent(
            user.id,
            agent.id
        )

        # =========================
        # 2. 获取长期摘要
        # =========================
        long_summary = get_summary(
            user.id,
            agent.id,
            db
        )

        # =========================
        # 3. 获取相关记忆（RAG）
        # =========================
        relevant_memories = memory_manager.search_relevant_memories(
            user.id,
            agent.id,
            message
        )

        # =========================
        # 4. 构建 Prompt
        # =========================
        # 构建工具调用提示
        tools_prompt = ""

        for tool in tool_registry.list_tools():

            tools_prompt += (
                f"工具名称:{tool['name']}\n"
                f"工具说明:{tool['description']}\n\n"
            )

        messages = []

        # 长期摘要
        if long_summary:
            messages.append({
                "role": "system",
                "content": f"用户长期记忆摘要：{long_summary}"
            })

        # Agent设定
        messages.append({
            "role": "system",
            "content": agent.system_prompt
        })

        # RAG相关记忆
        if relevant_memories:

            memory_text = "\n".join([
                f"{m['role']}: {m['content']}"
                for m in relevant_memories
            ])

            messages.append({
                "role": "system",
                "content": f"以下是与当前问题相关的历史记忆：\n{memory_text}"
            })

        # 短期记忆
        for h in short_histories:
            messages.append({
                "role": h["role"],
                "content": h["content"]
            })
        
        messages.append({
            "role": "system",
            "content":
                "你可以调用工具。\n"
                "如果需要调用工具，请严格返回JSON。\n\n"
                + tools_prompt +
                """
        格式：
        {
            "tool":"calculator",
            "arguments":{
                "expression":"2+2"
            }
        }
        """
        })

        # 当前用户消息
        messages.append({
            "role": "user",
            "content": message
        })

        # =========================
        # 5. 第一次调用LLM
        # =========================

        response = client.chat.completions.create(
            model="qwen-max",
            messages=messages
        )

        llm_output = response.choices[0].message.content

        # =========================
        # 6. 尝试解析工具调用
        # =========================

        tool_result = None

        try:

            tool_call = json.loads(
                llm_output
            )

            tool_name = tool_call["tool"]

            arguments = tool_call["arguments"]

            print("Tool Name:", tool_name)
            print("Arguments:", arguments)

            tool_result = execute_tool_call(
                tool_name,
                arguments
            )

        except Exception as e:

            print("Tool Parse Error:", str(e))

        # =========================
        # 7. 如果调用工具成功
        # =========================

        if tool_result:

            messages.append({
                "role": "assistant",
                "content": llm_output
            })

            messages.append({
                "role": "system",
                "content": f"工具执行结果：{tool_result}"
            })

            second_response = client.chat.completions.create(
                model="qwen-max",
                messages=messages
            )

            ai_message = (
                second_response
                .choices[0]
                .message
                .content
            )

        else:

            ai_message = llm_output

        # =========================
        # 6. 保存用户消息
        # =========================
        memory_manager.add_message(
            user.id,
            agent.id,
            "user",
            message
        )

        # =========================
        # 7. 保存AI消息
        # =========================
        memory_manager.add_message(
            user.id,
            agent.id,
            "assistant",
            ai_message
        )

        # =========================
        # 8. 更新长期摘要
        # =========================
        summary_input = "\n".join([
            h["content"]
            for h in short_histories
        ] + [message, ai_message])

        summary_response = client.chat.completions.create(
            model="qwen-max",
            messages=[
                {
                    "role": "system",
                    "content": "将以下内容压缩为长期摘要，保留关键信息"
                },
                {
                    "role": "user",
                    "content": summary_input
                }
            ]
        )

        new_summary = (
            summary_response
            .choices[0]
            .message
            .content
        )

        update_summary(
            user.id,
            agent.id,
            new_summary,
            db
        )

        return ai_message

    finally:

        db.close()


def get_summary(
    user_id: int,
    agent_id: int,
    db
):

    summary_obj = db.query(
        MemorySummary
    ).filter(
        MemorySummary.user_id == user_id,
        MemorySummary.agent_id == agent_id
    ).first()

    if summary_obj:
        return summary_obj.summary

    return ""


def update_summary(
    user_id: int,
    agent_id: int,
    new_summary: str,
    db
):

    summary_obj = db.query(
        MemorySummary
    ).filter(
        MemorySummary.user_id == user_id,
        MemorySummary.agent_id == agent_id
    ).first()

    if summary_obj:

        summary_obj.summary = new_summary

    else:

        summary_obj = MemorySummary(
            user_id=user_id,
            agent_id=agent_id,
            summary=new_summary
        )

        db.add(summary_obj)

    db.commit()

