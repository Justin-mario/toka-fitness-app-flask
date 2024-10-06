import pytest
from datetime import datetime, timedelta
from app.services.workout_session_service import WorkoutSessionService
from app.services.instructor_service import InstructorService

def test_create_workout_session(session):
    instructor = InstructorService.create_instructor(
        name="John Instructor",
        email="john@example.com",
        password="password123",
        date_of_birth=datetime(1990, 1, 1).date(),
        specialty="Yoga"
    )
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    workout_session = WorkoutSessionService.create_workout_session(
        title="Yoga Class",
        start_time=start_time,
        end_time=end_time,
        instructor_id=instructor.id
    )
    assert workout_session.title == "Yoga Class"
    assert workout_session.instructor.name == "John Instructor"

def test_get_all_workout_sessions(session):
    instructor = InstructorService.create_instructor(
        name="John Instructor",
        email="john@example.com",
        password="password123",
        date_of_birth=datetime(1990, 1, 1).date(),
        specialty="Yoga"
    )
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    WorkoutSessionService.create_workout_session(
        title="Yoga Class 1",
        start_time=start_time,
        end_time=end_time,
        instructor_id=instructor.id
    )
    WorkoutSessionService.create_workout_session(
        title="Yoga Class 2",
        start_time=start_time + timedelta(days=1),
        end_time=end_time + timedelta(days=1),
        instructor_id=instructor.id
    )
    sessions = WorkoutSessionService.get_all_workout_sessions()
    assert len(sessions) == 2
    assert sessions[0].title == "Yoga Class 1"
    assert sessions[1].title == "Yoga Class 2"

def test_get_workout_session_by_id(session):
    instructor = InstructorService.create_instructor(
        name="John Instructor",
        email="john@example.com",
        password="password123",
        date_of_birth=datetime(1990, 1, 1).date(),
        specialty="Yoga"
    )
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    workout_session = WorkoutSessionService.create_workout_session(
        title="Yoga Class",
        start_time=start_time,
        end_time=end_time,
        instructor_id=instructor.id
    )
    fetched_session = WorkoutSessionService.get_workout_session_by_id(workout_session.id)
    assert fetched_session.title == "Yoga Class"
    assert fetched_session.instructor.name == "John Instructor"

def test_update_workout_session(session):
    instructor1 = InstructorService.create_instructor(
        name="John Instructor",
        email="john@example.com",
        password="password123",
        date_of_birth=datetime(1990, 1, 1).date(),
        specialty="Yoga"
    )
    instructor2 = InstructorService.create_instructor(
        name="Jane Instructor",
        email="jane@example.com",
        password="password456",
        date_of_birth=datetime(1995, 1, 1).date(),
        specialty="Pilates"
    )
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    workout_session = WorkoutSessionService.create_workout_session(
        title="Yoga Class",
        start_time=start_time,
        end_time=end_time,
        instructor_id=instructor1.id
    )
    updated_session = WorkoutSessionService.update_workout_session(
        workout_session.id,
        title="Updated Pilates Class",
        instructor_id=instructor2.id
    )
    assert updated_session.title == "Updated Pilates Class"
    assert updated_session.instructor.name == "Jane Instructor"

def test_delete_workout_session(session):
    instructor = InstructorService.create_instructor(
        name="John Instructor",
        email="john@example.com",
        password="password123",
        date_of_birth=datetime(1990, 1, 1).date(),
        specialty="Yoga"
    )
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    workout_session = WorkoutSessionService.create_workout_session(
        title="Yoga Class",
        start_time=start_time,
        end_time=end_time,
        instructor_id=instructor.id
    )
    WorkoutSessionService.delete_workout_session(workout_session.id)
    assert WorkoutSessionService.get_workout_session_by_id(workout_session.id) is None

def test_get_sessions_by_instructor(session):
    instructor = InstructorService.create_instructor(
        name="John Instructor",
        email="john@example.com",
        password="password123",
        date_of_birth=datetime(1990, 1, 1).date(),
        specialty="Yoga"
    )
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    WorkoutSessionService.create_workout_session(
        title="Yoga Class 1",
        start_time=start_time,
        end_time=end_time,
        instructor_id=instructor.id
    )
    WorkoutSessionService.create_workout_session(
        title="Yoga Class 2",
        start_time=start_time + timedelta(days=1),
        end_time=end_time + timedelta(days=1),
        instructor_id=instructor.id
    )
    sessions = WorkoutSessionService.get_sessions_by_instructor(instructor.id)
    assert len(sessions) == 2
    assert all(session.instructor.id == instructor.id for session in sessions)