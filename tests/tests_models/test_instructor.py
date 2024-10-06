import pytest
from datetime import date, datetime, timedelta

from sqlalchemy.exc import IntegrityError

from app.models.instructor import Instructor
from app.models.workout_session import WorkoutSession


def test_new_instructor(session):
    """
    GIVEN an Instructor model
    WHEN a new Instructor is created
    THEN check the name, email, password, date_of_birth, and specialty fields are defined correctly
    """
    instructor = Instructor(
        name='Jane Instructor',
        email='jane@example.com',
        password='instructorpassword',
        date_of_birth=date(1985, 5, 15),
        specialty='Yoga'
    )
    session.add(instructor)
    session.commit()

    assert instructor.name == 'Jane Instructor'
    assert instructor.email == 'jane@example.com'
    assert instructor.password == 'instructorpassword'
    assert instructor.date_of_birth == date(1985, 5, 15)
    assert instructor.specialty == 'Yoga'

def test_add_duplicate_instructor(session):
    """
    GIVEN an Instructor already exist in the db
    WHEN the Instructor is added to the db again
    THEN give an error message
    """
    instructor = Instructor(
        name='Jane Instructor',
        email='jane@example.com',
        password='instructorpassword',
        date_of_birth=date(1985, 5, 15),
        specialty='Yoga'
    )
    session.add(instructor)
    session.commit()

    assert instructor.name == 'Jane Instructor'
    assert instructor.email == 'jane@example.com'
    assert instructor.password == 'instructorpassword'
    assert instructor.date_of_birth == date(1985, 5, 15)
    assert instructor.specialty == 'Yoga'


    instructor2 = Instructor(
        name='Jane Instructor 2',
        email='jane@example.com',  # Same email as instructor1
        password='password456',
        date_of_birth=date(1990, 1, 1),
        specialty='Pilates'
    )

    with pytest.raises(IntegrityError):
        session.add(instructor2)
        session.commit()



def test_instructor_representation(session):
    """
    GIVEN an Instructor model
    WHEN a new Instructor is created
    THEN check the string representation
    """
    instructor = Instructor(
        name='John Instructor',
        email='john@example.com',
        password='anotherpassword',
        date_of_birth=date(1980, 3, 20),
        specialty='Pilates'
    )
    session.add(instructor)
    session.commit()

    assert str(instructor) == 'Instructor: John Instructor (Specialty: Pilates)'

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