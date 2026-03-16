import pytest


@pytest.mark.asyncio
async def test_get_quiz_returns_questions(client, monkeypatch):
    from service.endpoints import data_handlers as dh

    class FakeQM:
        def __init__(self, session):
            pass

        async def get_questions_with_answers(self, params):
            return {1: {"id": 1, "text": "q1", "active": 1, "answers": []}}

    monkeypatch.setattr(dh, "QuestionsManager", FakeQM)

    resp = await client.get("/v1/quiz")
    assert resp.status_code == 200
    data = resp.json()
    assert "1" in data
    assert data["1"]["id"] == 1


@pytest.mark.asyncio
async def test_get_quiz_no_data_returns_empty(client, monkeypatch):
    from service.endpoints import data_handlers as dh

    class FakeQMNone:
        def __init__(self, session):
            pass

        async def get_questions_with_answers(self, params):
            return None

    monkeypatch.setattr(dh, "QuestionsManager", FakeQMNone)

    resp = await client.get("/v1/quiz")
    assert resp.status_code == 200
    assert resp.json() == {}


@pytest.mark.asyncio
async def test_get_questions_returns_list(client, monkeypatch):
    from service.endpoints import data_handlers as dh

    class FakeQM:
        def __init__(self, session):
            pass

        async def get_questions(self, data):
            return [
                {
                    "id": 1,
                    "text": "q1",
                    "active": 1,
                    "updated_dt": "2025-01-01T00:00:00Z",
                }
            ]

    monkeypatch.setattr(dh, "QuestionsManager", FakeQM)

    resp = await client.get(
        "/v1/questions?question_id=1&text=text+text&active=1"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["id"] == 1


@pytest.mark.asyncio
async def test_get_questions_empty_list(client, monkeypatch):
    from service.endpoints import data_handlers as dh

    class FakeQM:
        def __init__(self, session):
            pass

        async def get_questions(self, data):
            return []

    monkeypatch.setattr(dh, "QuestionsManager", FakeQM)

    resp = await client.get("/v1/questions")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert not data


@pytest.mark.asyncio
async def test_get_questions_handler(client):
    params = {
        "question_id": 1,
        "text": "Sample question?",
        "active": 1,
        # "order": "id",
        # "offset": 0,
        # "limit": 50,
    }
    resp = await client.get(
        "/v1/questions" + "?" + "&".join(f"{k}={v}" for k, v in params.items())
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert not data
