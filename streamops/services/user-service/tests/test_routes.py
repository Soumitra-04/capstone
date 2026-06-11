def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "user-service"


def test_register_user(client):
    response = client.post("/users/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_register_duplicate_user(client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass123"
    }
    client.post("/users/register", json=user_data)
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 400


def test_login_user(client):
    client.post("/users/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "mypassword"
    })
    response = client.post("/users/login", json={
        "username": "loginuser",
        "password": "mypassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "loginuser"
    assert data["message"] == "Login successful"


def test_login_invalid_credentials(client):
    response = client.post("/users/login", json={
        "username": "noexist",
        "password": "wrongpass"
    })
    assert response.status_code == 401


def test_get_user(client):
    reg = client.post("/users/register", json={
        "username": "getuser",
        "email": "get@example.com",
        "password": "pass123"
    })
    user_id = reg.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "getuser"


def test_get_user_not_found(client):
    response = client.get("/users/nonexistent-id")
    assert response.status_code == 404


def test_list_users(client):
    client.post("/users/register", json={
        "username": "user1",
        "email": "user1@example.com",
        "password": "pass"
    })
    client.post("/users/register", json={
        "username": "user2",
        "email": "user2@example.com",
        "password": "pass"
    })
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2
