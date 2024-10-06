from app._init_ import db
from datetime import datetime
from sqlalchemy.orm import validates

class WorkoutSession(db.Model):
    __tablename__ = 'workout_sessions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False)

    instructor = db.relationship('Instructor', back_populates='workout_sessions')

    @validates('end_time')
    def validate_end_time(self, key, end_time):
        if end_time <= self.start_time:
            raise ValueError("End time must be after start time")
        return end_time

    def __repr__(self):
        return f"WorkoutSession: {self.title} ({self.start_time})"