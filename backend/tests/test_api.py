from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_articles_returns_mock_catalog() -> None:
    response = client.get("/api/v1/articles")

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["source_url"] == "https://diversa.org.br/"


def test_chat_returns_answer_and_relevant_sources_for_profile() -> None:
    response = client.post(
        "/api/v1/chat",
        json={"message": "Como apoiar um estudante autista?", "profile": "familia"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["profile"] == "familia"
    assert "família" in payload["answer"]
    assert payload["sources"][0]["id"] == "mock-tea"


def test_chat_returns_no_sources_for_out_of_scope_question() -> None:
    response = client.post(
        "/api/v1/chat",
        json={"message": "Como estará o clima amanhã?"},
    )

    assert response.status_code == 200
    assert response.json()["sources"] == []


def test_chat_rejects_blank_message() -> None:
    response = client.post("/api/v1/chat", json={"message": "  "})

    assert response.status_code == 422
