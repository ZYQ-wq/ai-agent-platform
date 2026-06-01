from app.tools.base_tool import BaseTool


class SearchTool(BaseTool):

    name = "search"

    description = "搜索互联网信息"

    def run(
        self,
        keyword: str
    ):

        print(
            f"SearchTool被调用: {keyword}"
        )

        return f"模拟搜索结果：{keyword}"