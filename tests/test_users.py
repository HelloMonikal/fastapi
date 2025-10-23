
from app import schemas
import pytest
from jose import jwt
from app.config import settings

# tests should independ on each other

# def test_root(client):

#     response = client.get("/")
#     # print(f"打印输出在这：{response} and {response.json()}")
#     assert response.status_code == 200
#     assert response.json().get('message') == 'Hello World and Good luck! and goodmorning!'


def test_creater_user(client):
    response = client.post(
        "/users/"
        ,json={"email":"george2@gmail.com","password":"password123"}
    )
    new_user = schemas.UserOut(**response.json())
    # print(response.json())
    assert new_user.email == "george2@gmail.com"
    assert response.status_code == 201


def test_login_user(client,test_user):

    response = client.post(
        "/login/"
        ,data={"username":test_user["email"],"password":test_user["password"]}
    )
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token,
                         settings.secret_key,
                         algorithms=[settings.algorithm])
    id = payload.get('user_id')
    email = payload.get('user_email')
    assert id == test_user['id']
    assert email == test_user['email']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


# # @pytest.mark.parametrize
# def test_failed_login_user(client,test_user):

#     response = client.post(
#         "/login/"
#         ,data={"username":test_user["email"],"password":"wrongpassword"}
#     )
#     assert response.status_code == 403
#     assert response.json().get('detail') == "Invalid Credentials"



@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('george2@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('george2@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'