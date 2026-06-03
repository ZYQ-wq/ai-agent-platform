# app/runtime/workflow_engine.py
from app.runtime.context import WorkflowContext
from app.runtime.executors import NODE_REGISTRY

class WorkflowEngine:

    def __init__(self, nodes, edges, inputs=None):
        self.nodes = nodes
        self.edges = edges

        self.nodes_dict = {
            n["node_id"]: n for n in nodes
        }

        self.edges = edges

        # ⭐ 新增：全局上下文
        self.context = WorkflowContext()

        # ⭐ 新增：初始化 inputs
        self.inputs = inputs or {}

        # 放入上下文（关键）
        self.context.set("__inputs__", self.inputs)

    def find_start_node(self):
        """
        简单策略：找 node_type == start 的节点
        """
        for node in self.nodes_dict.values():
            if node['node_type'] == "start":
                return node['node_id']
        # 如果没有 start 节点，随便取第一个
        return list(self.nodes_dict.keys())[0]

    def next_node(self, current_node_id):
        """
        根据 edges 找下一个节点
        假设单链（MVP-1）
        """
        for edge in self.edges:
            if edge['source_node'] == current_node_id:
                return edge['target_node']
        return None

    def run(self):
        trace = []

        current_node_id = self.find_start_node()

        while current_node_id:

            node = self.nodes_dict[current_node_id]
            executor_cls = NODE_REGISTRY[node["node_type"]]

            # ⭐ 关键：获取上游节点输出
            upstream_output = self.get_upstream_output(current_node_id)

            executor = executor_cls(
                node,
                self.context,
                upstream_output   # ⭐ 新增
            )

            output = executor.run()

            self.context.set(current_node_id, output)

            trace.append({
                "node_id": current_node_id,
                "node_name": node["name"],
                "node_type": node["node_type"],
                "output": output
            })

            current_node_id = self.next_node(current_node_id)

        return {
            "trace": trace,
            "context": self.context.all()
        }
    
    def get_prev_node(self, node_id):

        for edge in self.edges:

            if edge["target_node"] == node_id:

                return edge["source_node"]

        return None
    
    def get_upstream_output(self, node_id):
        for edge in self.edges:
            if edge["target_node"] == node_id:
                source = edge["source_node"]
                return self.context.get(source)
        return None