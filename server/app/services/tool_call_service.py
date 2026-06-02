import json
from app.models.tool_call import ToolCall
from app.core.database import SessionLocal
from app.tools.registry import tool_registry


def execute_tool_call(
    tool_name,
    arguments
):

    tool = tool_registry.get(tool_name)

    if not tool:

        return None

    return tool.run(
        **arguments
    )

def log_tool_call(user_id, agent_id, tool_name, arguments, result):
    db = SessionLocal()
    try:
        call = ToolCall(
            user_id=user_id,
            agent_id=agent_id,
            tool_name=tool_name,
            arguments=json.dumps(arguments),
            result=str(result)
        )
        db.add(call)
        db.commit()
        db.refresh(call)
        return call
    finally:
        db.close()