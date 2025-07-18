from app.models import Task

def test_create_task(client, auth_headers):
    res = client.post("/tasks/", headers=auth_headers, json={
        "description": "Test task",
        "due_date": "2025-07-18T10:00:00"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["description"] == "Test task"
    assert data["is_completed"] is False

def test_get_tasks(client, auth_headers):
    # Create one task first
    client.post("/tasks/", headers=auth_headers, json={
        "description": "Fetch this"
    })

    res = client.get("/tasks/", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1

# def test_update_task(client, auth_headers):
#     # Create task
#     res = client.post("/tasks/", headers=auth_headers, json={"description": "to be updated"})
#     task_id = res.get_json()["id"]

#     # Update it
#     update = client.put(f"/tasks/{task_id}", headers=auth_headers, json={
#         "description": "Updated task",
#         "is_completed": True
#     })
#     assert update.status_code == 200

# def test_delete_task(client, auth_headers):
#     # Create a task
#     res = client.post("/tasks/", headers=auth_headers, json={"description": "to be deleted"})
#     task_id = res.get_json()["id"]

#     # Delete it
#     delete = client.delete(f"/tasks/{task_id}", headers=auth_headers)
#     assert delete.status_code == 200
#     assert delete.get_json()["msg"] == "Task deleted"
