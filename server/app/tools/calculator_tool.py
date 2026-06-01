from app.tools.base_tool import BaseTool


class CalculatorTool(BaseTool):

    name = "calculator"

    description = "执行数学计算"

    parameters = {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "数学表达式"
            }
        },
        "required": ["expression"]
    }

    def run(self, expression: str):

        print(
            f"CalculatorTool被调用: {expression}"
        )

        try:

            result = eval(
                expression,
                {"__builtins__": {}},
                {}
            )

            return str(result)

        except Exception as e:

            return f"计算失败:{str(e)}"