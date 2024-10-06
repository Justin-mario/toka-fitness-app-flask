import pytest
from datetime import date
from app.services.instructor_service import InstructorService
from app.models.workout_session import WorkoutSession

def test_create_instructor(session):
    instructor = InstructorService.create_instructor(
        name="John Doe",
        email="john@example.com",
        password="password123",
        date_of_birth=date(1990, 1, 1),
        specialty="Yoga"
    )
    assert instructor.name == "John Doe"
    assert instructor.email == "john@example.com"
    assert instructor.specialty == "Yoga"

def test_create_duplicate_instructor(session):
    InstructorService.create_instructor(
        name="John Doe",
        email="john@example.com",
        password="password123",
        date_of_birth=date(1990, 1, 1),
        specialty="Yoga"
    )
    with pytest.raises(ValueError, match="An instructor with this email already exists."):
        InstructorService.create_instructor(
            name="Jane Doe",
            email="john@example.com",
            password="password456",
            date_of_birth=date(1995, 1, 1),
            specialty="Pilates"
        )

def test_get_all_instructors(session):
    InstructorService.create_instructor(
        name="John Doe",
        email="john@example.com",
        password="password123",
        date_of_birth=date(1990, 1, 1),
        specialty="Yoga"
    )
    InstructorService.create_instructor(
        name="Jane Doe",
        email="jane@example.com",
        password="password456",
        date_of_birth=date(1995, 1, 1),
        specialty="Pilates"
    )
    instructors = InstructorService.get_all_instructors()
    assert len(instructors) == 2
    assert instructors[0].name == "John Doe"
    assert instructors[1].name == "Jane Doe"

def test_get_instructor_by_id(session):
    instructor = InstructorService.create_instructor(
        name="John Doe",
        email="john@example.com",
        password="password123",
        date_of_birth=date(1990, 1, 1),
        specialty="Yoga"
    )
    fetched_instructor = InstructorService.get_instructor_by_id(instructor.id)
    assert fetched_instructor.name == "John Doe"
    assert fetched_instructor.email == "john@example.com"

def test_update_instructor(session):
    instructor = InstructorService.create_instructor(
        name="John Doe",
        email="john@example.com",
        password="password123",
        date_of_birth=date(1990, 1, 1),
        specialty="Yoga"
    )
    updated_instructor = InstructorService.update_instructor(
        instructor.id,
        name="John Updated",
        specialty="Pilates"
    )
    assert updated_instructor.name == "John Updated"
    assert updated_instructor.specialty == "Pilates"
    assert updated_instructor.email == "john@example.com"  # Unchanged

def test_delete_instructor(session):
    instructor = InstructorService.create_instructor(
        name="John Doe",
        email="john@example.com",
        password="password123",
        date_of_birth=date(1990, 1, 1),
        specialty="Yoga"
    )
    InstructorService.delete_instructor(instructor.id)
    assert InstructorService.get_instructor_by_id(instructor.id) is None

def test_add_workout_session(session):
    instructor = InstructorService.create_instructor(
        name="John Doe",
        email="john@example.com",
        password="password123",
        date_of_birth=date(1990, 1, 1),
        specialty="Yoga"
    )
    workout_session = WorkoutSession(
        title="Yoga Class",
        start_time=date(2023, 6, 1),
        end_time=date(2023, 6, 2)
    )
    InstructorService.add_workout_session(instructor.id, workout_session)
    sessions = InstructorService.get_instructor_workout_sessions(instructor.id)
    assert len(sessions) == 1
    assert sessions[0].title == "Yoga Class"
