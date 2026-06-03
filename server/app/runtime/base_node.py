# app/runtime/base_node.py
from abc import ABC, abstractmethod

class BaseNode:
    def __init__(self, node_data, context, upstream_output=None):
        self.node_data = node_data
        self.context = context
        self.upstream_output = upstream_output

    @abstractmethod
    def run(self):
        """
        执行节点逻辑
        """
        pass