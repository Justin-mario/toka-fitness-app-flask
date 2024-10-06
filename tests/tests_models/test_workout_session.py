import pytest
from datetime import datetime, timedelta
from app.models.workout_session import WorkoutSession
from app.models.instructor import Instructor

def test_new_workout_session(session):
    """
    GIVEN a WorkoutSession model
    WHEN a new WorkoutSession is created
    THEN check the title, start_time, end_time, and instructor fields are defined correctly
    """
    instructor = Instructor(
        name="Jane Instructor",
        email="jane@example.com",
        password="password",
        date_of_birth=datetime(1990, 1, 1).date(),
        specialty="Yoga"
    )
    session.add(instructor)
    session.commit()

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)

    workout_session = WorkoutSession(
        title="Yoga Class",
        start_time=start_time,
        end_time=end_time,
        instructor=instructor
    )
    session.add(workout_session)
    session.commit()

    assert workout_session.title == "Yoga Class"
    assert workout_session.start_time == start_time
    assert workout_session.end_time == end_time
    assert workout_session.instructor == instructor
    assert workout_session.instructor.specialty == "Yoga"

def test_workout_session_representation(session):
    """
    GIVEN a WorkoutSession model
    WHEN a new WorkoutSession is created
    THEN check the string representation
    """
    instructor = Instructor(
        name="John Instructor",
        email="john@example.com",
        password="password",
        date_of_birth=datetime(1985, 1, 1).date(),
        specialty="Pilates"
    )
    session.add(instructor)
    session.commit()

    workout_session = WorkoutSession(
        title="Pilates Class",
        start_time=datetime(2023, 6, 1, 10, 0),
        end_time=datetime(2023, 6, 1, 11, 0),
        instructor=instructor
    )
    session.add(workout_session)
    session.commit()

    assert str(workout_session) == "WorkoutSession: Pilates Class (2023-06-01 10:00:00)"

def test_workout_session_end_time_validation(session):
    """
    GIVEN a WorkoutSession model
    WHEN a new WorkoutSession is created with end_time before start_time
    THEN it should raise a ValueError
    """
    instructor = Instructor(
        name="Test Instructor",
        email="test@example.com",
        password="password",
        date_of_birth=datetime(1990, 1, 1).date(),
        specialty="General"
    )
    session.add(instructor)
    session.commit()

    start_time = datetime.now()
    end_time = start_time - timedelta(hours=1)

    with pytest.raises(ValueError, match="End time must be after start time"):
        workout_session = WorkoutSession(
            title="Invalid Session",
            start_time=start_time,
            end_time=end_time,
            instructor=instructor
        )
        session.add(workout_session)
        session.commit()


def test_add_workout_session(session):
    """
    GIVEN an Instructor model and a WorkoutSession model
    WHEN a new WorkoutSession is added to an Instructor
    THEN check the WorkoutSession is correctly associated with the Instructor
    """
    instructor = Instructor(
        name='Jane Doe',
        email='jane@example.com',
        password='password123',
        date_of_birth=datetime(1990, 1, 1).date(),
        specialty='Yoga'
    )
    session.add(instructor)
    session.commit()

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    workout_session = WorkoutSession(
        title='Yoga Class',
        start_time=start_time,
        end_time=end_time
    )

    instructor.add_workout_session(workout_session)
    session.commit()

    assert workout_session in instructor.workout_sessions
    assert len(instructor.workout_sessions) == 1
    assert instructor.workout_sessions[0].title == 'Yoga Class'

def test_get_all_workout_sessions(session):
    """
    GIVEN an Instructor model with multiple WorkoutSessions
    WHEN retrieving all WorkoutSessions for the Instructor
    THEN check all WorkoutSessions are correctly retrieved
    """
    instructor = Instructor(
        name='John Smith',
        email='john@example.com',
        password='password456',
        date_of_birth=datetime(1985, 5, 15).date(),
        specialty='Pilates'
    )
    session.add(instructor)
    session.commit()

    start_time1 = datetime.now()
    end_time1 = start_time1 + timedelta(hours=1)
    workout_session1 = WorkoutSession(
        title='Pilates Class 1',
        start_time=start_time1,
        end_time=end_time1
    )

    start_time2 = start_time1 + timedelta(hours=2)
    end_time2 = start_time2 + timedelta(hours=1)
    workout_session2 = WorkoutSession(
        title='Pilates Class 2',
        start_time=start_time2,
        end_time=end_time2
    )

    instructor.add_workout_session(workout_session1)
    instructor.add_workout_session(workout_session2)
    session.commit()

    sessions = instructor.get_all_workout_sessions()
    assert len(sessions) == 2
    assert workout_session1 in sessions
    assert workout_session2 in sessions

