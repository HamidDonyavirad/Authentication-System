
def test_signup_access(client):

    user_test = {
        "email": "test@email.com",
        "password": "123456789hd",
    }
    response = client.post("/auth/signup", json=user_test)
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["email"] == user_test["email"]
    assert "id" in response_data
    assert "password" not in response_data
    assert "hashed_password" not in response_data
    assert response_data["id"] > 0
    assert response_data["provider"] == "local"
    assert response_data["is_active"] is True
    assert "created_at" in response_data

def test_signup_duplicate_email(client):
    user_test = {
        "email": "test@email.com",
        "password": "123456789hd",
    }
    response = client.post("/auth/signup", json=user_test)
    assert response.status_code == 400

def test_signup_invalid_email (client):
    user_test = {
        "email": "test",
        "password": "123456789mr",
    }
    response = client.post("/auth/signup", json=user_test)
    assert response.status_code == 422


def test_signup_missing_email(client):
    user_test = {
        "password": "123456789",
    }
    response = client.post("/auth/signup", json=user_test)
    assert response.status_code == 422

def test_signup_missing_password (client):
    user_test = {
        "email": "test1@email.com"
    }
    response = client.post("/auth/signup", json=user_test)
    assert response.status_code == 422

def test_signup_short_password(client):
    user_test = {
        "email":"test2@email.com",
        "password":"123"
    }
    response = client.post("/auth/signup", json=user_test)
    assert response.status_code == 422