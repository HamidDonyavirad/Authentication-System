from datetime import datetime, timezone
from app.models.password_reset import PasswordResetToken
from app.models.user import User


def test_forget_password(client, db):
    user_test = {"email": "test@test.com", "password": "123456789"}

    signup_response = client.post("/auth/signup", json=user_test)
    assert signup_response.status_code == 201
    forget_response = client.post("/auth/forget-password", json={"email":user_test["email"]})
    assert forget_response.status_code == 200
    assert forget_response.json()["message"] == "If the email exists, a reset link has been sent."
    user = db.query(User).filter_by(email=user_test["email"]).first()
    reset_token = db.query(PasswordResetToken).filter_by(user_id=user.id).first()
    assert reset_token is not None
    assert reset_token.user_id == user.id
    assert reset_token.is_used is False
    assert reset_token.token is not None
    assert reset_token.expires_at is not None
    assert reset_token.expires_at > datetime.now(timezone.utc)


def test_forget_password_email_not_exists(client, db):
    user_test = {"email": "test6@test.com", "password": "123456789"}

    reset_token_before = db.query(PasswordResetToken).count()
    forget_response = client.post("/auth/forget-password", json={"email":user_test["email"]})
    assert forget_response.status_code == 200
    assert forget_response.json()["message"] == "If the email exists, a reset link has been sent."
    reset_token_after = db.query(PasswordResetToken).count()
    assert reset_token_before == reset_token_after
