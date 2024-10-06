from app._init_ import db
from app.models.instructor import Instructor
from sqlalchemy.exc import IntegrityError


class InstructorService:
    @staticmethod
    def create_instructor(name, email, password, date_of_birth, specialty):
        instructor = Instructor(name=name, email=email, password=password,
                                date_of_birth=date_of_birth, specialty=specialty)
        try:
            db.session.add(instructor)
            db.session.commit()
            return instructor
        except IntegrityError:
            db.session.rollback()
            raise ValueError("An instructor with this email already exists.")

    @staticmethod
    def get_all_instructors():
        return Instructor.query.all()

    @staticmethod
    def get_instructor_by_id(instructor_id):
        return Instructor.query.get(instructor_id)

    @staticmethod
    def update_instructor(instructor_id, name=None, email=None, specialty=None):
        instructor = Instructor.query.get(instructor_id)
        if not instructor:
            raise ValueError("Instructor not found.")

        if name:
            instructor.name = name
        if email:
            instructor.email = email
        if specialty:
            instructor.specialty = specialty

        try:
            db.session.commit()
            return instructor
        except IntegrityError:
            db.session.rollback()
            raise ValueError("An instructor with this email already exists.")

    @staticmethod
    def delete_instructor(instructor_id):
        instructor = Instructor.query.get(instructor_id)
        if not instructor:
            raise ValueError("Instructor not found.")

        db.session.delete(instructor)
        db.session.commit()

    @staticmethod
    def add_workout_session(instructor_id, workout_session):
        instructor = Instructor.query.get(instructor_id)
        if not instructor:
            raise ValueError("Instructor not found.")

        instructor.add_workout_session(workout_session)
        db.session.commit()

    @staticmethod
    def get_instructor_workout_sessions(instructor_id):
        instructor = Instructor.query.get(instructor_id)
        if not instructor:
            raise ValueError("Instructor not found.")

        return instructor.get_all_workout_sessions()