# app/runtime/context.py
class WorkflowContext:
    def __init__(self):
        self._data = {}

    def set(self, node_id: str, value):
        self._data[node_id] = value

    def get(self, node_id: str):
        return self._data.get(node_id)

    def all(self):
        return self._data