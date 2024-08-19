from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
import pytest
from alembic import command
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'  #be akharesh test ezafe krdim ke ye database jadid besaze
engine = create_engine(SQLALCHEMY_DATABASE_URL)
testingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @pytest.fixture()   in misaze bad dobare pak mikone ama halate payini ke miznim vaghti misaze pak nmikone mitonim bbinim chikar krdim dafe badi ke run mikonim aval pak mikone
# def client():
#     Base.metadata.create_all(bind=engine)
#     # run our code before we run our test
#     yield TestClient(app)
#     # run our code after we run our test
#     Base.metadata.drop_all(bind=engine)



@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db: Session = testingSessionLocal()
    try:
        yield db
    finally:
        db.close()



@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user2(client):
    user_data = {"email": "amiralba224455@gmail.com", "password": "password123"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email": "amiralba2244@gmail.com", "password": "password123"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
        }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {"title": "first post", "content": "first post content", "owner_id":
         test_user['id']},
         {"title": "second post", "content": "second post content", "owner_id":
          test_user['id']},
          {"title": "third post", "content": "third post content", "owner_id":
           test_user['id']},
           {"title": "third post", "content": "third post content", "owner_id":
           test_user2['id']},
           ]
    
    def create_post_model(post):
        return models.Post(**post)
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)

    # session.add_all([models.Post(title="first post", content="first post content"),
    #                  models.Post(title="second post", content="second post content"),
    #                  models.Post(title="third post", content="third post content")
    #                  ])


    session.commit()
    posts = session.query(models.Post).all()
    return posts

    