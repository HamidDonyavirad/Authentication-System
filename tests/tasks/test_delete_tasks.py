from app.models.task import Task



def test_delete_task_success(client,db,authenticated_user):

    access_token = authenticated_user.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    task_data = {
        "title": "test task",
        "description": "test description",
        "category": "test category",
    }
    task_response = client.post("/task", json=task_data, headers=headers)
    assert task_response.status_code == 200
    task_id = task_response.json()["id"]
    task_response = client.delete(f"/task/{task_id}", headers=headers)
    assert task_response.status_code == 200
    find_task = db.query(Task).filter(Task.id == task_id).first()
    assert find_task is None
    assert task_response.json() == {"message": "Task deleted"}


def test_delete_task_not_found(client,authenticated_user):

    access_token = authenticated_user.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    task_data = {
        "title": "test task",
        "description": "test description",
        "category": "test category",
    }
    task_response = client.post("/task", json=task_data, headers=headers)
    assert task_response.status_code == 200
    task_response = client.delete(f"/task/999", headers=headers)
    assert task_response.status_code == 404


def test_delete_task_other_user(client,authenticated_user):

    access_token = authenticated_user.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    task_data = {
        "title": "test task",
        "description": "test description",
        "category": "test category",
    }
    task_response = client.post("/task", json=task_data, headers=headers)
    assert task_response.status_code == 200
    task_id = task_response.json()["id"]
    task_response = client.delete(f"/task/{task_id}", headers=headers)
    assert task_response.status_code == 200

    user_test_2 = {
        "email": "test26@test.com",
        "password": "123456789",
    }
    signup_response = client.post("/auth/signup", json=user_test_2)
    assert signup_response.status_code == 201
    login_response = client.post("/auth/login", json=user_test_2)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    task_response = client.delete(f"/task/{task_id}", headers=headers)
    assert task_response.status_code == 404


def test_delete_task_deleted(client,authenticated_user):

    access_token = authenticated_user.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    task_data = {
        "title": "test task",
        "description": "test description",
        "category": "test category",
    }
    task_response = client.post("/task", json=task_data, headers=headers)
    assert task_response.status_code == 200
    task_id = task_response.json()["id"]
    task_response = client.delete(f"/task/{task_id}", headers=headers)
    assert task_response.status_code == 200
    task_get_response = client.get(f"/task/{task_id}", headers=headers)
    assert task_get_response.status_code == 404