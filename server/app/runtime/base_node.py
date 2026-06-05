from abc import ABC, abstractmethod

class BaseNode:

    def __init__(
        self,
        node_data,
        context,
        resolved_inputs=None
    ):
        self.node_data = node_data
        self.context = context

        # WorkflowEngine传进来的解析后输入
        self.resolved_inputs = (
            resolved_inputs or {}
        )

    @abstractmethod
    def run(self):
        pass