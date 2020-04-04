from fastapi.testclient import TestClient

from main import app

import pytest

client = TestClient(app)

@pytest.mark.parametrize("name", ["Damian", "Zenek", "Karolina"])
def test_patient(name):
	response = client.post("/patient", json={"name": f"{name}", "surname": "Nowak"})
	assert response.json()["patient"] == {"name": f"{name}", "surname": "Nowak"}
