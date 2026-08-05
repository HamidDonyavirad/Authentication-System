


def test_update_task_success(client):
    user_test = {
        "email": "test19@test.com",
        "password": "123456789",
    }
    signup_response = client.post("/auth/signup", json=user_test)
    assert signup_response.status_code == 201
    login_response = client.post("/auth/login", json=user_test)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    task_data = {
        "title": "test task",
        "description": "test description",
        "category": "test category",
    }
    updated_task_data= {
        "title": "new title",
        "completed": True,
    }
    task_response = client.post("/task", json=task_data, headers=headers)
    assert task_response.status_code == 200
    task_id = task_response.json()["id"]
    task_update_response = client.put(f"/task/{task_id}", json=updated_task_data, headers=headers)
    assert task_update_response.status_code == 200
    data = task_update_response.json()
    assert data["title"] == "new title"
    assert data["description"] == "test description"
    assert data["category"] == "test category"
    assert data["completed"] is True


def test_update_task_not_found(client):
    user_test = {
        "email": "test20@test.com",
        "password": "123456789",
    }
    signup_response = client.post("/auth/signup", json=user_test)
    assert signup_response.status_code == 201
    login_response = client.post("/auth/login", json=user_test)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    task_data = {
        "title": "test task",
        "description": "test description",
        "category": "test category",
    }
    updated_task_data = {
        "title": "new title",
        "completed": True,
    }
    task_response = client.post("/task", json=task_data, headers=headers)
    assert task_response.status_code == 200
    task_update_response = client.put(f"/task/999", json=updated_task_data, headers=headers)
    assert task_update_response.status_code == 404


def test_update_task_other_user(client):
    user_test = {
        "email": "test21@test.com",
        "password": "123456789"
    }
    signup_response = client.post("/auth/signup", json=user_test)
    assert signup_response.status_code == 201
    login_response = client.post("/auth/login", json=user_test)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    task_data = {
        "title": "test task",
        "description": "test description",
        "category": "test category",
    }
    task_response = client.post("/task", json=task_data, headers=headers)
    assert task_response.status_code == 200
    task_id = task_response.json()["id"]

    user_test_2 = {
        "email": "test22@test.com",
        "password": "123456789"
    }
    signup_response = client.post("/auth/signup", json=user_test_2)
    assert signup_response.status_code == 201
    login_response = client.post("/auth/login", json=user_test_2)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    updated_task_data= {
        "title": "new title",
    }
    task_response = client.put(f"/task/{task_id}",json=updated_task_data, headers=headers)
    assert task_response.status_code == 404
