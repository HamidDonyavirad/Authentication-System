

def test_get_tasks_success(client):
    user_test = {
        "email":"test11@test.com",
        "password":"123456789",
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
    task_response = client.get("/task",headers=headers)
    assert task_response.status_code == 200
    data = task_response.json()
    assert len(data) == 1
    assert "id" in data[0]
    assert data[0]["title"] == "test task"
    assert data[0]["description"] == "test description"
    assert data[0]["category"] == "test category"
    assert data[0]["completed"] is False


def test_get_tasks_empty(client):
    user_test = {
        "email":"test12@test.com",
        "password":"123456789",
    }
    signup_response = client.post("/auth/signup", json=user_test)
    assert signup_response.status_code == 201
    login_response = client.post("/auth/login", json=user_test)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    task_response = client.get("/task",headers=headers)
    assert task_response.status_code == 200
    data = task_response.json()
    assert len(data) == 0
    assert type(data) is list

def test_get_tasks_filter_completed(client):
    user_test = {
        "email":"test13@test.com",
        "password":"123456789",
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
    task_data_2 = {
        "title": "test task2",
        "description": "test description2",
        "category": "test category2",
    }
    updated_task_data_2 = {
        "completed": True,
    }
    task_response = client.post("/task", json=task_data, headers=headers)
    assert task_response.status_code == 200
    task_response = client.post("/task", json=task_data_2, headers=headers)
    assert task_response.status_code == 200
    task_id = task_response.json()["id"]
    task_response_update = client.put(f"/task/{task_id}", json=updated_task_data_2, headers=headers)
    assert task_response_update.status_code == 200
    task_response = client.get(f"/task?completed=True",headers=headers)
    assert task_response.status_code == 200
    data = task_response.json()
    assert "id" in data[0]
    assert data[0]["id"] == task_id
    assert data[0]["completed"] is True
    assert data[0]["title"] == "test task2"
    assert data[0]["description"] == "test description2"
    assert data[0]["category"] == "test category2"

def test_get_tasks_filter_completed_and_category(client):

    user_test = {
        "email": "test14@test.com",
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
    task_data_2 = {
        "title": "test task2",
        "description": "test description2",
        "category": "test category2",
    }
    updated_task_data_2 = {
        "completed": True,
    }
    task_response = client.post("/task", json=task_data, headers=headers)
    assert task_response.status_code == 200
    task_response = client.post("/task", json=task_data_2, headers=headers)
    assert task_response.status_code == 200
    task_id = task_response.json()["id"]
    task_response_update = client.put(f"/task/{task_id}", json=updated_task_data_2, headers=headers)
    assert task_response_update.status_code == 200
    params = {
        "completed": True,
        "category": "test category2"
    }
    task_response = client.get("/task", headers=headers, params=params)
    assert task_response.status_code == 200
    data = task_response.json()
    assert "id" in data[0]
    assert data[0]["id"] == task_id
    assert data[0]["completed"] is True
    assert data[0]["title"] == "test task2"
    assert data[0]["description"] == "test description2"
    assert data[0]["category"] == "test category2"


def test_get_task_success(client):
    user_test = {
        "email": "test15@test.com",
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
    task_response = client.post("/task", json=task_data, headers=headers)
    assert task_response.status_code == 200
    task_id = task_response.json()["id"]
    task_response = client.get(f"/task/{task_id}", headers=headers)
    assert task_response.status_code == 200
    data = task_response.json()
    assert "id" in data
    assert data["title"] == "test task"
    assert data["description"] == "test description"
    assert data["category"] == "test category"
    assert data["completed"] is False


def test_get_task_not_found(client):
    user_test = {
            "email": "test16@test.com",
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
    task_response = client.post("/task", json=task_data, headers=headers)
    assert task_response.status_code == 200

    task_response = client.get(f"/task/999", headers=headers)
    assert task_response.status_code == 404

def test_get_task_other_user(client):
    user_test = {
        "email":"test17@test.com",
        "password":"123456789"
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
        "email":"test18@test.com",
        "password":"123456789"
    }
    signup_response = client.post("/auth/signup", json=user_test_2)
    assert signup_response.status_code == 201
    login_response = client.post("/auth/login", json=user_test_2)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    task_response = client.get(f"/task/{task_id}", headers=headers)
    assert task_response.status_code == 404

    
