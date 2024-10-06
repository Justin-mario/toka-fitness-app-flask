import pytest
from datetime import date
from app.models.user import User

def test_new_user(session):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the name, email, password, and date_of_birth fields are defined correctly
    """
    user = User(
        name='John Doe',
        email='johndoe@example.com',
        password='securepassword',
        date_of_birth=date(1990, 1, 1)
    )
    session.add(user)
    session.commit()

    assert user.name == 'John Doe'
    assert user.email == 'johndoe@example.com'
    assert user.password == 'securepassword'
    assert user.date_of_birth == date(1990, 1, 1)

def test_user_representation(session):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the string representation
    """
    user = User(
        name='Jane Doe',
        email='janedoe@example.com',
        password='anothersecurepassword',
        date_of_birth=date(1995, 5, 5)
    )
    session.add(user)
    session.commit()

    assert str(user) == 'User: Jane Doe'