from app.tools.calculator_tool import CalculatorTool

from app.tools.search_tool import SearchTool


class ToolRegistry:

    def __init__(self):

        self.tools = {}

    def register(self, tool):

        self.tools[tool.name] = tool

    def get(self, name):

        return self.tools.get(name)

    def list_tools(self):

        return [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in self.tools.values()
        ]
    
    def get_openai_tools(self):

        tools = []

        for tool in self.tools.values():

            tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            })

        return tools


tool_registry = ToolRegistry()

tool_registry.register(
    CalculatorTool()
)
tool_registry.register(SearchTool())