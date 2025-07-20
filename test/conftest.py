import pytest
from app import create_app, db as _db
from flask_jwt_extended import create_access_token
from app.models import User, Task

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret"
    })
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture(scope='function', autouse=True)
def clean_db(app):
    """Automatically clean DB before each test."""
    with app.app_context():
        _db.session.remove()
        for tbl in reversed(_db.metadata.sorted_tables):
            _db.session.execute(tbl.delete())
        _db.session.commit()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_user():
    user = User(username="user1")
    user.set_password("123456")
    _db.session.add(user)
    _db.session.commit()
    return user

@pytest.fixture
def auth_headers(test_user):
    access_token = create_access_token(identity=str(test_user.id))
    return {"Authorization": f"Bearer {access_token}"}
