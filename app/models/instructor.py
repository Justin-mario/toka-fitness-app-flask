from app._init_ import db
from datetime import date

from app.models.workout_session import WorkoutSession


class Instructor(db.Model):
    __tablename__ = 'instructor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    specialty = db.Column(db.String(100), nullable=False)

    workout_sessions = db.relationship('WorkoutSession', back_populates='instructor')

    def __repr__(self):
        return f'Instructor: {self.name} (Specialty: {self.specialty})'

    def add_workout_session(self, workout_session):
        self.workout_sessions.append(workout_session)

    def get_all_workout_sessions(self):
        return self.workout_sessions

