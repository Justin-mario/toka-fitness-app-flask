from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api

db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title='Fitness App API',
    version='1.0',
    description='A simple fitness app API',
    doc='/swagger/'
)


def create_app(config_name='default'):
    app = Flask(__name__)

    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_app.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'  # Add this line

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    with app.app_context():
        from app import models
        db.create_all()

    from app.routes import register_routes
    register_routes(app, api)

    return app