from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.oauth2 import create_access_token
from app.config import settings
from app.database import get_db
from app import models
from app.database import  Base



SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@" \
                          f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Scope is important because it defines when the fixture runs. Default is function, meaning it will run for each
#   function but you can set it as needed
@pytest.fixture()
def session():
    """
    This will drop all tables in database, create tables and then return db session
    This is needed so we have a fresh database with each test
    This is used if you just want to access the database
    """
    # run our code after our test finishes
    Base.metadata.drop_all(bind=engine)
    # run our code before we run our test
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()    


@pytest.fixture()
def client(session):
    """
    This will get a db session and return a client
    This is used if you need access to the app client
    """

    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    # This will override get_db (dev db) with override_get_db (test db) so anytime get_db is referenced override_get_db will be used instead
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)  # TestClient works like the requests module


@pytest.fixture()
def test_user(client):
    """
    Create a test user that can be used in testing
    """
    res = client.post("/users/", json={"email": "hello@gmail.com", "password": "pass123"})
    new_user = res.json()
    new_user["password"] = "pass123"
    assert res.status_code == 201
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "hello123@gmail.com",
                 "password": "pass123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers, 
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture()
def test_posts(test_user, session, test_user2):
    posts_data = [
    {
        "title": "first title",
        "content": "first content",
        "owner_id": test_user["id"]
    },
    {
        "title": "second title",
        "content": "second content",
        "owner_id": test_user["id"]
    },
    {
        "title": "third title",
        "content": "third content",
        "owner_id": test_user["id"]
    }, 
    {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
