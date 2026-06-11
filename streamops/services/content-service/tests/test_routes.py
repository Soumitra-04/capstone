import uuid


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "content-service"


def test_create_game(client):
    response = client.post("/games", json={
        "name": "Valorant",
        "description": "5v5 tactical shooter"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Valorant"
    assert data["description"] == "5v5 tactical shooter"
    assert "id" in data


def test_create_duplicate_game(client):
    game_data = {"name": "Apex Legends", "description": "Battle royale"}
    client.post("/games", json=game_data)
    response = client.post("/games", json=game_data)
    assert response.status_code == 400


def test_list_games(client):
    client.post("/games", json={"name": "Game 1"})
    client.post("/games", json={"name": "Game 2"})
    response = client.get("/games")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_game(client):
    create_resp = client.post("/games", json={"name": "Fortnite", "description": "BR game"})
    game_id = create_resp.json()["id"]
    response = client.get(f"/games/{game_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Fortnite"


def test_get_game_not_found(client):
    response = client.get(f"/games/{uuid.uuid4()}")
    assert response.status_code == 404


def test_search_games(client):
    client.post("/games", json={"name": "Counter-Strike 2"})
    client.post("/games", json={"name": "Counter-Strike GO"})
    client.post("/games", json={"name": "Valorant"})
    response = client.get("/search?q=Counter")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_search_no_query(client):
    response = client.get("/search")
    assert response.status_code == 400


def test_recommendations(client):
    client.post("/games", json={"name": "Game A"})
    client.post("/games", json={"name": "Game B"})
    user_id = str(uuid.uuid4())
    response = client.get(f"/recommendations/{user_id}")
    assert response.status_code == 200
    recs = response.json()
    assert len(recs) == 2
    assert all(r["user_id"] == user_id for r in recs)


def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
