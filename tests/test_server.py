from __future__ import annotations

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from agent_se.server import app


client = TestClient(app)


def test_health_ok():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_run_and_memory(tmp_path):
    response = client.post(
        "/api/run",
        json={
            "goal": "Genera progetto demo",
            "project_dir": str(tmp_path / "workspace"),
            "max_iterations": 5,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["reports"]
    assert "memory" in payload


def test_chat_offline_mode():
    response = client.post(
        "/api/chat",
        json={
            "prompt": "Ciao agente",
            "model": "deepseek-ai/deepseek-v4-pro",
            "api_key": "",
        },
    )
    assert response.status_code == 200
    assert "OFFLINE MODE" in response.json()["content"]
