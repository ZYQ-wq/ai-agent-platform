import json

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