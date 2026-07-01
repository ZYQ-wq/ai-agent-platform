
from openai import OpenAI
import json
from typing import Generator

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
from app.services.tool_call_service import execute_tool_call,log_tool_call


client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)


def _prepare_chat_context(
    message: str,
    user_email: str,
    agent_id: int,
    db
):
    user = db.query(User).filter(
        User.email == user_email
    ).first()

    if not user:
        raise Exception("用户不存在")

    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.user_id == user.id
    ).first()

    if not agent:
        raise Exception("Agent不存在")

    memory_manager = MemoryManager()

    short_histories = memory_manager.get_recent(
        user.id,
        agent.id
    )

    long_summary = get_summary(
        user.id,
        agent.id,
        db
    )

    relevant_memories = memory_manager.search_relevant_memories(
        user.id,
        agent.id,
        message
    )

    messages = []

    if long_summary:
        messages.append({
            "role": "system",
            "content": f"用户长期记忆摘要：{long_summary}"
        })

    messages.append({
        "role": "system",
        "content": agent.system_prompt
    })

    if relevant_memories:
        memory_text = "\n".join([
            f"{m['role']}: {m['content']}"
            for m in relevant_memories
        ])

        messages.append({
            "role": "system",
            "content": f"以下是与当前问题相关的历史记忆：\n{memory_text}"
        })

    for h in short_histories:
        messages.append({
            "role": h["role"],
            "content": h["content"]
        })

    messages.append({
        "role": "user",
        "content": message
    })

    return {
        "user": user,
        "agent": agent,
        "messages": messages,
        "memory_manager": memory_manager,
        "short_histories": short_histories,
    }


def _accumulate_tool_calls(
    tool_calls_delta,
    accumulated: dict
):
    if not tool_calls_delta:
        return

    for tool_call in tool_calls_delta:
        index = tool_call.index

        if index not in accumulated:
            accumulated[index] = {
                "id": "",
                "name": "",
                "arguments": ""
            }

        if tool_call.id:
            accumulated[index]["id"] = tool_call.id

        if tool_call.function:
            if tool_call.function.name:
                accumulated[index]["name"] += tool_call.function.name
            if tool_call.function.arguments:
                accumulated[index]["arguments"] += tool_call.function.arguments


def _build_tool_call_message(
    accumulated: dict,
    content: str
):
    tool_calls = []

    for index in sorted(accumulated.keys()):
        item = accumulated[index]
        tool_calls.append({
            "id": item["id"],
            "type": "function",
            "function": {
                "name": item["name"],
                "arguments": item["arguments"]
            }
        })

    return {
        "role": "assistant",
        "content": content or None,
        "tool_calls": tool_calls
    }


def _stream_completion(
    messages: list,
    tools: list | None = None
) -> Generator[tuple[str, dict], None, None]:
    kwargs = {
        "model": "qwen-max",
        "messages": messages,
        "stream": True,
    }

    if tools is not None:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

    stream = client.chat.completions.create(**kwargs)

    full_content = ""
    tool_calls_accum: dict = {}

    for chunk in stream:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta

        if delta.content:
            full_content += delta.content
            yield ("content", {"delta": delta.content})

        _accumulate_tool_calls(
            delta.tool_calls,
            tool_calls_accum
        )

    yield ("complete", {
        "content": full_content,
        "tool_calls": tool_calls_accum
    })


def _persist_chat(
    ctx: dict,
    user_message: str,
    ai_message: str,
    db
):
    memory_manager = ctx["memory_manager"]
    user = ctx["user"]
    agent = ctx["agent"]
    short_histories = ctx["short_histories"]

    memory_manager.add_message(
        user.id,
        agent.id,
        "user",
        user_message
    )

    memory_manager.add_message(
        user.id,
        agent.id,
        "assistant",
        ai_message
    )

    summary_input = "\n".join([
        h["content"]
        for h in short_histories
    ] + [user_message, ai_message])

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


def stream_chat_with_agent(
    message: str,
    user_email: str,
    agent_id: int
) -> Generator[dict, None, None]:
    db = SessionLocal()

    try:
        ctx = _prepare_chat_context(
            message,
            user_email,
            agent_id,
            db
        )

        messages = list(ctx["messages"])
        user = ctx["user"]
        agent = ctx["agent"]

        first_result = {
            "content": "",
            "tool_calls": {}
        }

        for event_type, payload in _stream_completion(
            messages,
            tools=tool_registry.get_openai_tools()
        ):
            if event_type == "content":
                yield {
                    "type": "content",
                    "delta": payload["delta"]
                }
            elif event_type == "complete":
                first_result = payload

        ai_message = first_result["content"]

        if first_result["tool_calls"]:
            tool_call = first_result["tool_calls"][0]
            tool_name = tool_call["name"]
            arguments = json.loads(tool_call["arguments"])

            tool_result = execute_tool_call(
                tool_name,
                arguments
            )

            log_tool_call(
                user.id,
                agent.id,
                tool_name,
                arguments,
                tool_result
            )

            messages.append(
                _build_tool_call_message(
                    first_result["tool_calls"],
                    first_result["content"]
                )
            )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": str(tool_result)
            })

            ai_message = ""

            for event_type, payload in _stream_completion(messages):
                if event_type == "content":
                    ai_message += payload["delta"]
                    yield {
                        "type": "content",
                        "delta": payload["delta"]
                    }

        if not ai_message.strip():
            raise Exception("模型未返回有效内容")

        _persist_chat(ctx, message, ai_message, db)

        yield {
            "type": "done",
            "content": ai_message
        }

    finally:
        db.close()


def chat_with_agent(
    message,
    user_email,
    agent_id
):

    db = SessionLocal()

    try:

        ctx = _prepare_chat_context(
            message,
            user_email,
            agent_id,
            db
        )

        messages = ctx["messages"]
        user = ctx["user"]
        agent = ctx["agent"]

        response = client.chat.completions.create(
            model="qwen-max",
            messages=messages,
            tools=tool_registry.get_openai_tools(),
            tool_choice="auto"
        )

        message_obj = response.choices[0].message

        tool_calls = message_obj.tool_calls

        if tool_calls:

            tool_call = tool_calls[0]

            tool_name = tool_call.function.name
        
            arguments = json.loads(
                tool_call.function.arguments
            )

            tool_result = execute_tool_call(
                tool_name,
                arguments
            )

            log_tool_call(
                user.id,
                agent.id,
                tool_name,
                arguments,
                tool_result
            )
        
            messages.append(
                message_obj
            )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(tool_result)
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

            ai_message = message_obj.content

        _persist_chat(
            ctx,
            message,
            ai_message,
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

