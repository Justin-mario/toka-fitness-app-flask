from datetime import datetime, date

from app._init_ import db
from app.models.user import User
from sqlalchemy.exc import IntegrityError


class UserService:
    @staticmethod
    def create_user(name, email, password, date_of_birth):
        # Ensure date_of_birth is a datetime.date object
        if isinstance(date_of_birth, str):
            try:
                date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD")

        # Check if the user is at least 12 years old
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        if age < 12:
            raise ValueError("User must be at least 12 years old to register.")

        user = User(name=name, email=email, password=password, date_of_birth=date_of_birth)

        try:
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ValueError("A user with this email already exists.")

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def update_user(user_id, name=None, email=None):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found.")

        if name:
            user.name = name
        if email:
            user.email = email

        try:
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ValueError("A user with this email already exists.")

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found.")

        db.session.delete(user)
        db.session.commit()