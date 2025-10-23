from fastapi.testclient import TestClient
import pytest
from app.main import app
from sqlalchemy import create_engine
from app.database import Base
from app.database import get_db
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.oauth2 import create_token
from app import models

# SQLALCHEMY_DATABASE_URL  = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost:5432/fastapi_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TesstingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


# put override_get_db in fixture 
# def override_get_db():
#     db = TesstingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# kind of need to walk though these codes
@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TesstingSessionLocal()
    try:
        yield db
    finally: 
        db.close()


# set dependency on session
@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally: 
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)




@pytest.fixture
def test_user(client):
    user_data ={"email":"george2@gmail.com","password":"password123"}
    response = client.post("/users/",json=user_data)
    new_user = response.json()
    new_user["password"] = user_data["password"]
    assert response.status_code == 201
    return new_user


@pytest.fixture
def test_user2(client):
    user_data ={"email":"george3@gmail.com","password":"password123"}
    response = client.post("/users/",json=user_data)
    new_user = response.json()
    new_user["password"] = user_data["password"]
    assert response.status_code == 201
    return new_user



@pytest.fixture
def token(test_user):
    token = create_token({"user_id":test_user['id'],"user_email":test_user['email']})
    return token

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client



@pytest.fixture
def test_posts(test_user, session,test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },
    {
        "title": "4th title",
        "content": "4th content",
        "owner_id": test_user2['id']
    }
    
    ]

    def create_post_model(post):
        return models.Post(**post)

    posts = list(map(create_post_model, posts_data))
    session.add_all(posts)

    session.commit()

    posts = session.query(models.Post).all()

    return posts