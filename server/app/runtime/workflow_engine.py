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

        # 全局上下文
        self.context = WorkflowContext()

        # 初始化 inputs
        self.inputs = inputs or {}

        # 放入上下文
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
        根据 edges 找下一个节点（假设单链）
        """
        for edge in self.edges:
            if edge['source_node'] == current_node_id:
                return edge['target_node']
        return None

    def get_prev_node(self, node_id):
        for edge in self.edges:
            if edge["target_node"] == node_id:
                return edge["source_node"]
        return None

    def get_upstream_output(self, node_id):
        """
        保留原有方法（用于向后兼容）
        """
        for edge in self.edges:
            if edge["target_node"] == node_id:
                source = edge["source_node"]
                return self.context.get(source)
        return None

    def resolve_inputs(self, node):
        """
        解析节点的输入变量定义
        :param node: 节点字典
        :return: dict {input_name: resolved_value}
        """
        resolved = {}
        inputs_def = node.get("inputs", [])
        for inp in inputs_def:
            name = inp["name"]
            value_def = inp.get("value")
            if not value_def:
                # 没有 value 定义（如开始节点），跳过或置空
                resolved[name] = None
                continue

            kind = value_def.get("kind")
            raw_value = value_def.get("value")

            if kind == "constant":
                resolved[name] = raw_value
            elif kind == "variable":
                # 解析变量引用: 格式 "node_id.output_name"
                try:
                    src_node_id, output_field = raw_value.split(".", 1)
                except ValueError:
                    raise ValueError(f"Invalid variable reference: {raw_value}")

                # 从上下文中获取上游节点的输出
                upstream_output = self.context.get(src_node_id)
                if upstream_output is None:
                    raise ValueError(f"Upstream node '{src_node_id}' output not found for variable '{name}'")

                # 支持嵌套字段，如 "result.text"
                parts = output_field.split(".")
                current = upstream_output
                for part in parts:
                    if isinstance(current, dict):
                        current = current.get(part)
                    else:
                        # 如果上游输出不是字典，尝试直接属性访问
                        current = getattr(current, part, None)
                    if current is None:
                        raise ValueError(f"Field '{part}' not found in output of node '{src_node_id}'")
                resolved[name] = current
            else:
                raise ValueError(f"Unknown value kind: {kind}")

        return resolved

    def run(self):
        trace = []

        current_node_id = self.find_start_node()

        while current_node_id:
            node = self.nodes_dict[current_node_id]

            # 解析该节点的所有输入变量（常量/变量引用）
            resolved_inputs = self.resolve_inputs(node)

            # 获取 executor 类
            executor_cls = NODE_REGISTRY[node["node_type"]]

            # 创建 executor，传入解析后的输入（取代原来的 upstream_output）
            executor = executor_cls(node, self.context, resolved_inputs)

            output = executor.run()

            # 将节点输出存入全局上下文（供后续节点引用）
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