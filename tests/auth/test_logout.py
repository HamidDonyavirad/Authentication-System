from app.core.security import hash_refresh_token
from app.models.refresh_token import RefreshToken
from app.models.user import User



def test_logout_success(client, db,authenticated_user,user_test):
    refresh_token = authenticated_user.json()["refresh_token"]
    access_token = authenticated_user.json()["access_token"]
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
    

def test_logout_without_access_token(client, db,authenticated_user):
    refresh_token = authenticated_user.json()["refresh_token"]
    headers = {}
    json = {"refresh_token": refresh_token}
    response_logout = client.post("/auth/logout", headers=headers, json=json)
    assert response_logout.status_code == 401

def test_logout_invalid_refresh_token(client, db,authenticated_user):
    access_token = authenticated_user.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    json = {"refresh_token": "refresh_token1234"}
    response_logout = client.post("/auth/logout", headers=headers, json=json)
    assert response_logout.status_code == 401

def test_logout_twice(client, db,authenticated_user):
    refresh_token = authenticated_user.json()["refresh_token"]
    access_token = authenticated_user.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    json = {"refresh_token": refresh_token}
    response_logout = client.post("/auth/logout", headers=headers, json=json)
    assert response_logout.status_code == 204

    response_logout = client.post("/auth/logout", headers=headers, json=json)
    assert response_logout.status_code == 401