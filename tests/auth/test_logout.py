from app.core.security import hash_refresh_token
from app.models.refresh_token import RefreshToken
from app.models.user import User



def test_logout_success(client, db):
    user_test={"email":"test1@test.com","password":"123456789"}

    response_signup = client.post("/auth/signup",json=user_test)
    assert response_signup.status_code == 201
    response_login = client.post("/auth/login",json=user_test)
    assert response_login.status_code == 200

    refresh_token = response_login.json()["refresh_token"]
    access_token = response_login.json()["access_token"]
    headers = {"Authorization":f"Bearer {access_token}"}
    json = {"refresh_token":refresh_token}
    response_logout = client.post("/auth/logout",headers=headers,json=json)
    assert response_logout.status_code == 204
    hashed_refresh_token = hash_refresh_token(refresh_token)
    user = db.query(User).filter(User.email == user_test["email"]).first()
    assert user is not None
    token_record = db.query(RefreshToken).filter(
        RefreshToken.hashed_token == hashed_refresh_token,
        RefreshToken.user_id == user.id
    ).first()
    assert token_record is not None
    assert token_record.is_revoked is True
    

def test_logout_without_access_token(client, db):
    user_test = {"email": "test2@test.com", "password": "123456789"}

    response_signup = client.post("/auth/signup", json=user_test)
    assert response_signup.status_code == 201
    response_login = client.post("/auth/login", json=user_test)
    assert response_login.status_code == 200

    refresh_token = response_login.json()["refresh_token"]
    headers = {}
    json = {"refresh_token": refresh_token}
    response_logout = client.post("/auth/logout", headers=headers, json=json)
    assert response_logout.status_code == 401

def test_logout_invalid_refresh_token(client, db):
    user_test = {"email": "test3@test.com", "password": "123456789"}

    response_signup = client.post("/auth/signup", json=user_test)
    assert response_signup.status_code == 201
    response_login = client.post("/auth/login", json=user_test)
    assert response_login.status_code == 200

    access_token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    json = {"refresh_token": "refresh_token1234"}
    response_logout = client.post("/auth/logout", headers=headers, json=json)
    assert response_logout.status_code == 401

def test_logout_twice(client, db):
    user_test = {"email": "test4@test.com", "password": "123456789"}

    response_signup = client.post("/auth/signup", json=user_test)
    assert response_signup.status_code == 201
    response_login = client.post("/auth/login", json=user_test)
    assert response_login.status_code == 200

    refresh_token = response_login.json()["refresh_token"]
    access_token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    json = {"refresh_token": refresh_token}
    response_logout = client.post("/auth/logout", headers=headers, json=json)
    assert response_logout.status_code == 204

    response_logout = client.post("/auth/logout", headers=headers, json=json)
    assert response_logout.status_code == 401