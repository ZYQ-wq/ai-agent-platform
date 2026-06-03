# app/services/workflow_service.py

import json

from fastapi import HTTPException

from app.core.database import SessionLocal

from app.models.user import User
from app.models.workflow import Workflow
from app.models.workflow_node import WorkflowNode
from app.models.workflow_edge import WorkflowEdge
from app.runtime.workflow_engine import WorkflowEngine


def save_workflow_service(
    user_email: str,
    req
):

    db = SessionLocal()

    try:

        user = db.query(User).filter(
            User.email == user_email
        ).first()

        if not user:

            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )

        workflow = Workflow(
            user_id=user.id,
            name=req.name
        )

        db.add(workflow)
        db.commit()
        db.refresh(workflow)

        # 保存节点
        for node in req.nodes:

            workflow_node = WorkflowNode(
                workflow_id=workflow.id,
                node_id=node.node_id,
                node_type=node.node_type,
                name=node.name,
                config=json.dumps(
                    node.config,
                    ensure_ascii=False
                )
            )

            db.add(workflow_node)

        # 保存边
        for edge in req.edges:

            workflow_edge = WorkflowEdge(
                workflow_id=workflow.id,
                source_node=edge.source_node,
                target_node=edge.target_node
            )

            db.add(workflow_edge)

        db.commit()

        return {
            "message": "保存成功",
            "workflow_id": workflow.id
        }

    finally:

        db.close()


def get_workflows_service(
    user_email: str
):

    db = SessionLocal()

    try:

        user = db.query(User).filter(
            User.email == user_email
        ).first()

        if not user:

            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )

        workflows = db.query(
            Workflow
        ).filter(
            Workflow.user_id == user.id
        ).all()

        return workflows

    finally:

        db.close()


def get_workflow_detail_service(
    workflow_id: int,
    user_email: str
):

    db = SessionLocal()

    try:

        user = db.query(User).filter(
            User.email == user_email
        ).first()

        workflow = db.query(
            Workflow
        ).filter(
            Workflow.id == workflow_id,
            Workflow.user_id == user.id
        ).first()

        if not workflow:

            raise HTTPException(
                status_code=404,
                detail="工作流不存在"
            )

        nodes = db.query(
            WorkflowNode
        ).filter(
            WorkflowNode.workflow_id == workflow.id
        ).all()

        edges = db.query(
            WorkflowEdge
        ).filter(
            WorkflowEdge.workflow_id == workflow.id
        ).all()

        return {
            "id": workflow.id,
            "name": workflow.name,
            "nodes": [
                {
                    "node_id": n.node_id,
                    "node_type": n.node_type,
                    "name": n.name,
                    "config": json.loads(
                        n.config or "{}"
                    )
                }
                for n in nodes
            ],
            "edges": [
                {
                    "source_node": e.source_node,
                    "target_node": e.target_node
                }
                for e in edges
            ]
        }

    finally:

        db.close()


def delete_workflow_service(
    workflow_id: int,
    user_email: str
):

    db = SessionLocal()

    try:

        user = db.query(User).filter(
            User.email == user_email
        ).first()

        workflow = db.query(
            Workflow
        ).filter(
            Workflow.id == workflow_id,
            Workflow.user_id == user.id
        ).first()

        if not workflow:

            raise HTTPException(
                status_code=404,
                detail="工作流不存在"
            )

        db.query(
            WorkflowNode
        ).filter(
            WorkflowNode.workflow_id == workflow.id
        ).delete(
            synchronize_session=False
        )

        db.query(
            WorkflowEdge
        ).filter(
            WorkflowEdge.workflow_id == workflow.id
        ).delete(
            synchronize_session=False
        )

        db.delete(workflow)

        db.commit()

        return {
            "message": "删除成功"
        }

    finally:

        db.close()

def run_workflow_service(
        workflow_id: int, 
        user_email: str, 
        inputs: dict
):
    workflow = get_workflow_detail_service(workflow_id, user_email)

    nodes = workflow['nodes']
    edges = workflow['edges']

    from app.runtime.workflow_engine import WorkflowEngine

    engine = WorkflowEngine(nodes=nodes, edges=edges, inputs=inputs)
    result = engine.run()  # 返回 trace + context

    return {
        "status": "success",
        "workflow_id": workflow_id,
        "workflow_name": workflow['name'],
        "result": result
    }