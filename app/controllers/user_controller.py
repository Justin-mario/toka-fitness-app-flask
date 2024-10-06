from flask import request, jsonify
from app.services.user_service import UserService
from app._init_ import db
from datetime import datetime

class UserController:
    @staticmethod
    def register():
        data = request.json if request.is_json else request.form

        try:
            user = UserService.create_user(
                name=data['name'],
                email=data['email'],
                password=data['password'],
                date_of_birth=data['date_of_birth']
            )
            return jsonify({
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'date_of_birth': user.date_of_birth.isoformat()
                }
            }), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An error occurred while registering the user'}), 500