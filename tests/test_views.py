import pytest
from rest_framework.test import APIClient

from shortener.models import ShortURL

LONG_URL = "http://example.com/very-very/long/url/even-longer"

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


def test_shorten_creates_short_url(client):
    response = client.post("/api/shorten/", {"url": LONG_URL}, format="json")

    assert response.status_code == 201
    short = ShortURL.objects.get()
    assert short.url == LONG_URL
    assert response.json() == {"short_url": f"http://testserver/shrt/{short.code}"}


def test_shorten_same_url_twice_returns_same_short_url(client):
    first = client.post("/api/shorten/", {"url": LONG_URL}, format="json")
    second = client.post("/api/shorten/", {"url": LONG_URL}, format="json")

    assert second.status_code == 200
    assert first.json() == second.json()
    assert ShortURL.objects.count() == 1


def test_shorten_invalid_url_returns_400(client):
    response = client.post("/api/shorten/", {"url": "nope"}, format="json")

    assert response.status_code == 400
    assert "url" in response.json()


def test_expand_returns_original_url(client):
    ShortURL.objects.create(url=LONG_URL, code="aZ3kQ9x")

    response = client.post(
        "/api/expand/", {"short_url": "http://testserver/shrt/aZ3kQ9x"}, format="json"
    )

    assert response.status_code == 200
    assert response.json() == {"url": LONG_URL}


def test_expand_unknown_code_returns_404(client):
    response = client.post(
        "/api/expand/", {"short_url": "http://testserver/shrt/missing"}, format="json"
    )

    assert response.status_code == 404


def test_expand_invalid_input_returns_400(client):
    response = client.post("/api/expand/", {"short_url": "http://example.com/x"}, format="json")

    assert response.status_code == 400


@pytest.mark.parametrize("path", ["/shrt/aZ3kQ9x", "/shrt/aZ3kQ9x/"])
def test_follow_redirects_to_original(client, path):
    ShortURL.objects.create(url=LONG_URL, code="aZ3kQ9x")

    response = client.get(path)

    assert response.status_code == 302
    assert response["Location"] == LONG_URL


def test_follow_unknown_code_returns_404(client):
    assert client.get("/shrt/missing").status_code == 404
