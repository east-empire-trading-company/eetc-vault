import pytest

from main import app


@pytest.fixture(scope="function")
def client():
    app.testing = True
    return app.test_client()
