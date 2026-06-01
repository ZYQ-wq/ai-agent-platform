from app.tools.base_tool import BaseTool

from app.services.search_service import tavily_search


class SearchTool(BaseTool):

    name = "search"

    description = "搜索互联网信息"

    parameters = {
        "type": "object",
        "properties": {
            "keyword": {
                "type": "string",
                "description": "搜索关键词"
            }
        },
        "required": ["keyword"]
    }

    def run(
        self,
        keyword: str
    ):

        print(
            f"SearchTool被调用: {keyword}"
        )

        result = tavily_search(keyword)

        return str(result)