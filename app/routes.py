from flask import render_template, request, redirect, url_for, flash
from flask_restx import Resource, fields
from app.controllers.user_controller import UserController

def register_routes(app, api):
    # API routes
    ns = api.namespace('users', description='User operations')

    user_model = api.model('User', {
        'name': fields.String(required=True, description='User name'),
        'email': fields.String(required=True, description='User email'),
        'password': fields.String(required=True, description='User password'),
        'date_of_birth': fields.Date(required=True, description='User date of birth')
    })

    @ns.route('/register')
    class UserRegister(Resource):
        @ns.expect(user_model)
        @ns.response(201, 'User successfully created')
        @ns.response(400, 'Validation error')
        def post(self):
            """Register a new user via API"""
            return UserController.register()

    # HTML routes
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            result = UserController.register()
            if isinstance(result, tuple) and result[1] == 201:
                flash('Registration successful!', 'success')
                return redirect(url_for('register'))
            else:
                flash('Registration failed. Please try again.', 'error')
        return render_template('templates/register.html')