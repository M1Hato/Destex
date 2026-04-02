import pytest
from app.models.user_model import User
from app.repositories.task_repo import TaskRepo
from app.schemas.task_schemas import TaskCreate
from app.models.task_model import Task

@pytest.mark.asyncio
async def test_create_task_in_db(db_session):
    #fake user
    test_user = User(email="test@mail.com", username="tester", password="hash")
    db_session.add(test_user)
    await db_session.commit()
    await db_session.refresh(test_user)

    #create a task
    task_schema = TaskCreate(
        title="Integration Task",
        description="Testing DB",
        priority="Medium",
        deadline="2026-05-05T10:00:00"
    )
    task_model = Task(**task_schema.model_dump(), user_id=test_user.id)

    new_task = await TaskRepo.create_task_repo(task_model, test_user.id, db_session)

    assert new_task.id is not None
    assert new_task.title == "Integration Task"