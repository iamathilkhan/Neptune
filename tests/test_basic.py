import os
import json

def test_index_and_api_chat():
    os.environ["NEPTUNE_SKIP_BUILD"] = "1"

    from app import app as flask_app
    flask_app.config["TESTING"] = True

    client = flask_app.test_client()
    r = client.get("/")
    assert r.status_code == 200

    context = {
        "tdrop": 28,
        "tbar": 1013,
        "tskinice": 25,
        "rainocn": 0.3,
        "delts": 0.5,
        "latitude": 15.0,
        "longitude": 75.0
    }
    payload = {"query": "Is it good to fish?", "context_data": context}
    r2 = client.post("/api/chat", data=json.dumps(payload), content_type="application/json")
    assert r2.status_code == 200
    data = r2.get_json()
    assert "response" in data
