from fastapi.testclient import TestClient

from app.main import app

import pytest

client = TestClient(app)

@pytest.mark.parametrize("name", ["Damian", "Zenek", "Karolina"])
def test_patient(name):
	response = client.post("/patient", json={"name": f"{name}", "surename": "Nowak"})
	assert response.json()["patient"] == {"name": f"{name}", "surename": "Nowak"}


def test_get_patient():
	response = client.get("/patient/0")
	assert response.json() == {"name": "Damian", "surename": "Nowak"}
