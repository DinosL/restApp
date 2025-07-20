def test_register(client):
    res = client.post("/register", json={
        "username": "user1",
        "password": "123456"
    })
    assert res.status_code == 201
    assert res.get_json()["msg"] == "User created"

def test_login_success(client):
    client.post("/register", json={"username": "user1", "password": "123456"})
    res = client.post("/login", json={
        "username": "user1",
        "password": "123456"
    })
    assert res.status_code == 200
    assert "access_token" in res.get_json()

def test_login_failure(client):
    res = client.post("/login", json={
        "username": "user2",
        "password": "67891011"
    })
    assert res.status_code == 401
