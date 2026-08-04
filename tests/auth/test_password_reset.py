from datetime import datetime, timedelta, timezone
from app.core.security import verify_password
from app.models.password_reset import PasswordResetToken
from app.models.user import User

def test_password_reset_success(client,db):
    user_test = {"email": "test7@test.com", "password": "123456789"}

    signup_response = client.post("/auth/signup", json=user_test)
    assert signup_response.status_code == 201
    forget_response = client.post("/auth/forget-password", json={"email": user_test["email"]})
    assert forget_response.status_code == 200
    assert forget_response.json()["message"] == "If the email exists, a reset link has been sent."
    user = db.query(User).filter_by(email=user_test["email"]).first()
    reset_token = db.query(PasswordResetToken).filter_by(user_id=user.id).first()
    token = reset_token.token
    new_password = "123456789987"
    reset_response = client.post("/auth/reset-password", json={"token": token, "new_password": new_password})
    assert reset_response.status_code == 200
    assert reset_response.json()["message"] == "Password changed successfully"
    # Reload entities from the database after the endpoint commits.
    db.expire_all()
    reset_token = db.query(PasswordResetToken).filter_by(user_id=user.id).first()
    user = db.query(User).filter_by(email=user_test["email"]).first()
    assert reset_token.is_used is True
    assert verify_password(new_password, user.hashed_password) is True


def test_reset_password_invalid_token(client):
    token = "fake-token"
    new_password = "12345678987"
    reset_response = client.post("/auth/reset-password", json={"token": token, "new_password": new_password})
    assert reset_response.status_code == 400
    assert reset_response.json()["detail"] == "Invalid token"

def test_reset_password_used_token(client,db):
    user_test = {"email": "test8@test.com", "password": "123456789"}

    signup_response = client.post("/auth/signup", json=user_test)
    assert signup_response.status_code == 201
    forget_response = client.post("/auth/forget-password", json={"email": user_test["email"]})
    assert forget_response.status_code == 200
    assert forget_response.json()["message"] == "If the email exists, a reset link has been sent."
    user = db.query(User).filter_by(email=user_test["email"]).first()
    reset_token = db.query(PasswordResetToken).filter_by(user_id=user.id).first()
    token = reset_token.token
    new_password = "123456789987"
    reset_response = client.post("/auth/reset-password", json={"token": token, "new_password": new_password})
    assert reset_response.status_code == 200
    assert reset_response.json()["message"] == "Password changed successfully"
    reset_response_twice = client.post("/auth/reset-password", json={"token": token, "new_password": new_password})
    assert reset_response_twice.status_code == 400
    assert reset_response_twice.json()["detail"] == "Token already used"


def test_reset_password_expired_token(client,db):
    user_test = {"email": "test9@test.com", "password": "123456789"}

    signup_response = client.post("/auth/signup", json=user_test)
    assert signup_response.status_code == 201
    forget_response = client.post("/auth/forget-password", json={"email": user_test["email"]})
    assert forget_response.status_code == 200
    assert forget_response.json()["message"] == "If the email exists, a reset link has been sent."
    user = db.query(User).filter_by(email=user_test["email"]).first()
    reset_token = db.query(PasswordResetToken).filter_by(user_id=user.id).first()
    reset_token.expires_at = datetime.now(timezone.utc) - timedelta(hours=1)
    db.commit()
    token = reset_token.token
    new_password = "123456789987"
    reset_response = client.post("/auth/reset-password", json={"token": token, "new_password": new_password})
    assert reset_response.status_code == 400
    assert reset_response.json()["detail"] == "Token expired"




