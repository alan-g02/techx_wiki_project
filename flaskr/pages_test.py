from flaskr import create_app
import pytest


# See https://flask.palletsprojects.com/en/2.2.x/testing/
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_about_page(client):
    resp = client.get("/about")
    assert resp.status_code == 200


def test_upload_page(client):
    resp = client.get("/upload")
    assert resp.status_code == 200
