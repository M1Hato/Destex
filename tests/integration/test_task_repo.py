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


@pytest.mark.asyncio
async def test_get_tasks_privacy(db_session):
    #create users
    user_a = User(email="a@mail.com", username="user_a", password="hash")
    user_b = User(email="b@mail.com", username="user_b", password="hash")
    db_session.add_all([user_a, user_b])
    await db_session.commit()
    await db_session.refresh(user_a)

    #create task
    task_a = Task(title="Task A", user_id=user_a.id, priority="LOW", is_deleted=False)
    task_b = Task(title="Task B", user_id=user_b.id, priority="HIGH", is_deleted=False)
    db_session.add_all([task_a, task_b])

    await db_session.commit()

    tasks_for_a = await TaskRepo.get_user_task_repo(
        user_id=user_a.id,
        offset=0,
        limit=10,
        search=None,
        priority="LOW",
        session=db_session
    )

    assert len(tasks_for_a) == 1
    assert tasks_for_a[0].title == "Task A"