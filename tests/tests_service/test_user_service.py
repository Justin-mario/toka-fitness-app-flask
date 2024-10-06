import pytest
from datetime import date
from app.services.user_service import UserService

def test_create_user(session):
    user = UserService.create_user(
        name="John Doe",
        email="john@example.com",
        password="password123",
        date_of_birth=date(1990, 1, 1)
    )
    assert user.name == "John Doe"
    assert user.email == "john@example.com"

def test_create_duplicate_user(session):
    UserService.create_user(
        name="John Doe",
        email="john@example.com",
        password="password123",
        date_of_birth=date(1990, 1, 1)
    )
    with pytest.raises(ValueError, match="A user with this email already exists."):
        UserService.create_user(
            name="Jane Doe",
            email="john@example.com",
            password="password456",
            date_of_birth=date(1995, 1, 1)
        )

def test_get_all_users(session):
    UserService.create_user(
        name="John Doe",
        email="john@example.com",
        password="password123",
        date_of_birth=date(1990, 1, 1)
    )
    UserService.create_user(
        name="Jane Doe",
        email="jane@example.com",
        password="password456",
        date_of_birth=date(1995, 1, 1)
    )
    users = UserService.get_all_users()
    assert len(users) == 2
    assert users[0].name == "John Doe"
    assert users[1].name == "Jane Doe"

def test_get_user_by_id(session):
    user = UserService.create_user(
        name="John Doe",
        email="john@example.com",
        password="password123",
        date_of_birth=date(1990, 1, 1)
    )
    fetched_user = UserService.get_user_by_id(user.id)
    assert fetched_user.name == "John Doe"
    assert fetched_user.email == "john@example.com"

def test_update_user(session):
    user = UserService.create_user(
        name="John Doe",
        email="john@example.com",
        password="password123",
        date_of_birth=date(1990, 1, 1)
    )
    updated_user = UserService.update_user(
        user.id,
        name="John Updated",
        email="johnupdated@example.com"
    )
    assert updated_user.name == "John Updated"
    assert updated_user.email == "johnupdated@example.com"

def test_delete_user(session):
    user = UserService.create_user(
        name="John Doe",
        email="john@example.com",
        password="password123",
        date_of_birth=date(1990, 1, 1)
    )
    UserService.delete_user(user.id)
    assert UserService.get_user_by_id(user.id) is None