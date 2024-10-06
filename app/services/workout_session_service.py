from app._init_ import db
from app.models.workout_session import WorkoutSession
from app.models.instructor import Instructor
from sqlalchemy.exc import IntegrityError


class WorkoutSessionService:
    @staticmethod
    def create_workout_session(title, start_time, end_time, instructor_id):
        instructor = Instructor.query.get(instructor_id)
        if not instructor:
            raise ValueError("Instructor not found.")

        workout_session = WorkoutSession(title=title, start_time=start_time, end_time=end_time, instructor=instructor)
        db.session.add(workout_session)
        db.session.commit()
        return workout_session

    @staticmethod
    def get_all_workout_sessions():
        return WorkoutSession.query.all()

    @staticmethod
    def get_workout_session_by_id(session_id):
        return WorkoutSession.query.get(session_id)

    @staticmethod
    def update_workout_session(session_id, title=None, start_time=None, end_time=None, instructor_id=None):
        workout_session = WorkoutSession.query.get(session_id)
        if not workout_session:
            raise ValueError("Workout session not found.")

        if title:
            workout_session.title = title
        if start_time:
            workout_session.start_time = start_time
        if end_time:
            workout_session.end_time = end_time
        if instructor_id:
            instructor = Instructor.query.get(instructor_id)
            if not instructor:
                raise ValueError("Instructor not found.")
            workout_session.instructor = instructor

        db.session.commit()
        return workout_session

    @staticmethod
    def delete_workout_session(session_id):
        workout_session = WorkoutSession.query.get(session_id)
        if not workout_session:
            raise ValueError("Workout session not found.")

        db.session.delete(workout_session)
        db.session.commit()

    @staticmethod
    def get_sessions_by_instructor(instructor_id):
        return WorkoutSession.query.filter_by(instructor_id=instructor_id).all()