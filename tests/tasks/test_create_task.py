from app.models.task import Task


def test_create_task_success(client,db):
    user_test = {
        "email":"test10@test.com",
        "password":"123456789",
    }

    signup_response = client.post("/auth/signup",json=user_test)
    assert signup_response.status_code == 201
    login_response = client.post("/auth/login",json=user_test)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    task_data = {
        "title": "test task",
        "description":"test description",
        "category":"test category",
    }
    task_response = client.post("/task",json=task_data,headers=headers)
    assert task_response.status_code == 200
    data = task_response.json()
    assert data["title"] == "test task"
    assert data["description"] == "test description"
    assert data["category"] == "test category"
    assert data["completed"] is False

    task = db.query(Task).filter(Task.id == data["id"]).first()
    assert task is not None
    assert task.owner_id is not None
    assert task.title == task_data["title"]


def test_create_task_unauthorized(client):
    task_data = {
        "title": "test task",
        "description": "test description",
        "category": "test category",
    }
    task_response = client.post("/task",json=task_data)
    assert task_response.status_code == 401


