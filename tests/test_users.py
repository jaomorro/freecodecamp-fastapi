import pytest
from jose import jwt
from app import schemas
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     print(res.json())
#     assert res.json().get("message") == "Hello World"
#     assert res.status_code ==200



def test_crete_user(client):
    # Trailing / in /users/ is important because fastapi will redirect /users to /users/ but in doing so the status code
    #   will be 307 instead of 201, which will cause the test to fail
    res = client.post("/users/", json={"email": "hello@gmail.com", "password": "pass123"})
    # print(res.json())
    new_user = schemas.UserOut(**res.json()) # this will check to see if the output matches the required schema
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert test_user["id"] == id
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "pass123", 403),
    ("jimmy@gmail.com", "wrongpassword", 403),
    ("wrongemail@gmail.com", "wrongpassword", 403),
    (None, "pass123", 422), # 422 is schema validation error
    ("jimmy@gmail.com", None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password, "status_code": status_code})

    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"