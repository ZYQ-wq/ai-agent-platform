# app/runtime/executors.py

from .base_node import BaseNode
from app.runtime.llm_client import call_qwen

# =========================
# Start Node
# =========================

class StartNode(BaseNode):

    def run(self):

        workflow_inputs = self.context.get(
            "__inputs__"
        )

        print(
            f"Start Node {self.node_data['node_id']} executed"
        )

        return workflow_inputs or {}


# =========================
# LLM Node
# =========================

class LLMNode(BaseNode):
    def run(self):
        config = self.node_data.get("config", {})
        prompt = None

        # 优先用上游节点的输出
        if isinstance(self.upstream_output, dict):
            prompt = self.upstream_output.get("prompt")

        # fallback
        if not prompt:
            prompt = config.get("prompt", "")
        if not prompt:
            prompt = self.context.get("__inputs__", {}).get("prompt", "")

        result = call_qwen(prompt)
        return result

# =========================
# Tool Node
# =========================

class ToolNode(BaseNode):

    def run(self):

        print(
            f"Tool Node {self.node_data['node_id']} executed"
        )

        return {
            "tool_result": "success"
        }


# =========================
# Output Node
# =========================

class OutputNode(BaseNode):
    def run(self):
        # 获取前一个节点输出
        # MVP 假设单前驱
        prev_node_id = self.node_data.get("prev_node_id")
        if prev_node_id is None:
            # 没有显式配置prev_node_id，则自动取上下文最后一个节点的输出
            # 排序取最后一个
            keys = [k for k in self.context.all().keys() if k.isdigit()]
            keys.sort(key=int)
            prev_node_id = keys[-1]

        output = self.context.get(prev_node_id)
        print(f"Output Node {self.node_data['node_id']} value: {output}")
        return output


# =========================
# Registry
# =========================

NODE_REGISTRY = {
    "start": StartNode,
    "llm": LLMNode,
    "tool": ToolNode,
    "output": OutputNode,
}