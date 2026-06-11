import uuid


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "stream-service"


def test_create_stream(client):
    response = client.post("/streams", json={
        "streamer_id": str(uuid.uuid4()),
        "game_id": str(uuid.uuid4()),
        "game_name": "Valorant",
        "title": "Ranked Grind"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Ranked Grind"
    assert data["is_live"] is True
    assert data["viewer_count"] == 0


def test_list_streams(client):
    client.post("/streams", json={
        "streamer_id": str(uuid.uuid4()),
        "title": "Stream 1"
    })
    client.post("/streams", json={
        "streamer_id": str(uuid.uuid4()),
        "title": "Stream 2"
    })
    response = client.get("/streams")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_stream(client):
    create_resp = client.post("/streams", json={
        "streamer_id": str(uuid.uuid4()),
        "title": "My Stream"
    })
    stream_id = create_resp.json()["id"]
    response = client.get(f"/streams/{stream_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "My Stream"


def test_get_stream_not_found(client):
    response = client.get(f"/streams/{uuid.uuid4()}")
    assert response.status_code == 404


def test_update_viewers(client):
    create_resp = client.post("/streams", json={
        "streamer_id": str(uuid.uuid4()),
        "title": "Viewer Test"
    })
    stream_id = create_resp.json()["id"]
    response = client.patch(f"/streams/{stream_id}/viewers", json={"viewer_count": 150})
    assert response.status_code == 200
    assert response.json()["viewer_count"] == 150


def test_end_stream(client):
    create_resp = client.post("/streams", json={
        "streamer_id": str(uuid.uuid4()),
        "title": "Ending Stream"
    })
    stream_id = create_resp.json()["id"]
    response = client.delete(f"/streams/{stream_id}")
    assert response.status_code == 200
    assert response.json()["is_live"] is False
    assert response.json()["ended_at"] is not None


def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
