# test_runtime.py
from app.runtime.workflow_engine import WorkflowEngine

nodes = [
    {"node_id": "1", "node_type": "start", "config": {"input": "hello"}},
    {"node_id": "2", "node_type": "llm", "config": {"prompt": "Say hi"}},
    {"node_id": "3", "node_type": "output", "config": {}}
]

edges = [
    {"source_node": "1", "target_node": "2"},
    {"source_node": "2", "target_node": "3"}
]

engine = WorkflowEngine(nodes, edges)
context = engine.run()
print("Workflow Execution Result:", context)