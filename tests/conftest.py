import pytest
from app._init_ import create_app, db

@pytest.fixture(scope='function')
def app():
    app = create_app('testing')
    return app

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def session(app):
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()