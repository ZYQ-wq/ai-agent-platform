# app/runtime/executors.py

from .base_node import BaseNode
from app.runtime.llm_client import call_qwen

# =========================
# Start Node
# =========================

class StartNode(BaseNode):
    def run(self):
        # 开始节点：输入来自工作流启动时的全局输入
        # 可以直接使用 resolved_inputs（其中已经包含了 __inputs__ 中的值）
        # 也可以从 context 获取
        workflow_inputs = self.context.get("__inputs__")
        print(f"Start Node {self.node_data['node_id']} executed")
        return workflow_inputs or {}


# =========================
# LLM Node
# =========================

class LLMNode(BaseNode):
    def run(self):
        config = self.node_data.get("config", {})
        prompt = None

        # 优先从解析后的输入中获取 prompt
        if self.resolved_inputs:
            prompt = self.resolved_inputs.get("prompt")

        # 如果解析输入中没有，再从 config 中获取（兼容旧数据）
        if not prompt:
            prompt = config.get("prompt", "")
        # 最后从全局输入中获取
        if not prompt:
            prompt = self.context.get("__inputs__", {}).get("prompt", "")

        result = call_qwen(prompt)
        return result


# =========================
# Tool Node
# =========================

class ToolNode(BaseNode):
    def run(self):
        # 可以从 resolved_inputs 中获取工具需要的参数
        query = self.resolved_inputs.get("query", "") if self.resolved_inputs else ""
        print(f"Tool Node {self.node_data['node_id']} executed with query: {query}")
        # 模拟工具执行
        return {"tool_result": f"Executed tool with query: {query}"}


# =========================
# Output Node
# =========================

class OutputNode(BaseNode):
    def run(self):
        # 输出节点通常只需要输出上游节点的结果
        # 可以从 resolved_inputs 中获得已经聚合的输入（如果有多个输入）
        # 或者从 context 中获取前一个节点的输出（单链情况）
        prev_node_id = self.node_data.get("prev_node_id")
        if prev_node_id is None:
            # 自动查找前一个节点：获取上下文中最近添加的节点输出（非 __inputs__）
            all_keys = [k for k in self.context.all().keys() if k != "__inputs__"]
            # 简单的假设：节点 ID 为数字字符串，按数字排序取最大
            numeric_keys = [k for k in all_keys if k.isdigit()]
            if numeric_keys:
                numeric_keys.sort(key=int)
                prev_node_id = numeric_keys[-1]
            elif all_keys:
                prev_node_id = all_keys[-1]
            else:
                prev_node_id = None

        if prev_node_id:
            output = self.context.get(prev_node_id)
        else:
            output = self.resolved_inputs  # 如果没有任何上游，就直接输出解析后的输入

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