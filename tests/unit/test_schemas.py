from datetime import datetime
import pytest
from pydantic import ValidationError
from app.schemas.task_schemas import TaskCreate
from app.schemas.user_schemas import UserCreate


def test_user_create_schema_is_valid():

    data = {"email": "testemail@gmail.com", "password": "123secret", "username": "testuser"}
    user = UserCreate(**data)

    assert user.email == "testemail@gmail.com"

def test_user_create_schema_invalid_email():
    data = {"email": "invalid-email", "password": "123secret", "username": "testuser"}
    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_task_create_schema_is_valid():
    data = {"title": "TestTask", "description": "This task is for test", "deadline": "2026-04-03T12:00:00", "priority": "Low"}

    task = TaskCreate(**data)
    assert task.title == "TestTask"
    expected_date = datetime(2026, 4, 3, 12, 0, 0)
    assert task.deadline == expected_date


def test_task_create_schema_invalid_date():
    data = {"title": "TestTask", "description": "This task is for test", "deadline": "2026-13-15T12:00",
            "priority": "Low"}

    with pytest.raises(ValidationError):
        TaskCreate(**data)