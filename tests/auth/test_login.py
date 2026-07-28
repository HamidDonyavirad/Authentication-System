
def test_login_success(client):
    user_test = {
        "email": "bagher@email.com",
        "password": "123456789"
    }
    user_create = client.post("/auth/signup", json=user_test)
    assert user_create.status_code == 201
    response = client.post("/auth/login", json=user_test)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.json()["access_token"]!=""
    assert response.json()["refresh_token"]!=""
    assert type(response.json()["access_token"]) == str
    assert type(response.json()["refresh_token"]) == str


def test_login_invalid_password(client):
    user_test = {
        "email": "test35@email.com",
        "password": "123456789"
    }
    user_test_invalid_password = {
        "email": "test3@email.com",
        "password": "1234567899"
    }
    response_signup = client.post("/auth/signup", json=user_test)
    response = client.post("/auth/login", json=user_test_invalid_password)
    assert response_signup.status_code == 201
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_wrong_email(client):
    user_test = {
        "email":"test1@email.com",
        "password": "123456789"
    }
    user_test_invalid_email = {
        "email":"test2@email.com",
        "password":"123456789"
    }
    response_signup = client.post("/auth/signup", json=user_test)
    response = client.post("/auth/login", json=user_test_invalid_email)
    assert response_signup.status_code == 201
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_invalid_email(client):
    user_test = {
        "email":"test5@email.com",
        "password":"123456789"
    }
    user_test_invalid_email = {
        "email":"not-an-email",
        "password":"123456789"
    }
    response_signup = client.post("/auth/signup", json=user_test)
    response = client.post("/auth/login", json=user_test_invalid_email)
    assert response_signup.status_code == 201
    assert response.status_code == 422

