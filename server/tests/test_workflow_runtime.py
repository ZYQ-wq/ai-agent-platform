from app.services.workflow_service import (
    get_workflow_detail_service
)

from app.runtime.workflow_engine import (
    WorkflowEngine
)


def test_workflow():

    workflow = get_workflow_detail_service(
        workflow_id=4,
        user_email="admin@test.com"
    )

    inputs = {"prompt": "介绍Transformer"}
    engine = WorkflowEngine(
        workflow["nodes"],
        workflow["edges"],
        inputs
    )
    result = engine.run()
    print(result)


if __name__ == "__main__":
    test_workflow()