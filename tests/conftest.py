import pytest
from fastapi.testclient import TestClient

from translator.app import app


@pytest.fixture
def client():
    return TestClient(app)  # Arrange (organização)
