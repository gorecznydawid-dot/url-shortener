import requests

LONG_URL = "http://example.com/very-very/long/url/even-longer"


def test_shorten_expand_and_follow(live_server):
    response = requests.post(f"{live_server.url}/api/shorten/", json={"url": LONG_URL})
    assert response.status_code == 201
    short_url = response.json()["short_url"]
    assert short_url.startswith(f"{live_server.url}/shrt/")

    response = requests.post(f"{live_server.url}/api/shorten/", json={"url": LONG_URL})
    assert response.json()["short_url"] == short_url

    response = requests.post(f"{live_server.url}/api/expand/", json={"short_url": short_url})
    assert response.status_code == 200
    assert response.json() == {"url": LONG_URL}

    response = requests.get(short_url, allow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == LONG_URL


def test_errors(live_server):
    response = requests.post(f"{live_server.url}/api/shorten/", json={"url": "ftp://example.com"})
    assert response.status_code == 400

    response = requests.post(
        f"{live_server.url}/api/expand/", json={"short_url": f"{live_server.url}/shrt/missing"}
    )
    assert response.status_code == 404

    response = requests.get(f"{live_server.url}/shrt/missing", allow_redirects=False)
    assert response.status_code == 404
