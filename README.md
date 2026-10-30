# URL shortener

Small URL shortening API in Django REST Framework.

## Running

```
docker compose up --build
```

The API is available at http://localhost:8000. Migrations run on container start.

## Tests

```
docker compose run --rm web pytest
```

Unit tests cover the code generator, serializers and views. `tests/test_e2e.py` starts a live server and goes through the whole flow over real HTTP with `requests`.

## API

Shorten a URL:

```
$ curl -X POST localhost:8000/api/shorten/ -H 'Content-Type: application/json' \
    -d '{"url": "http://example.com/very-very/long/url/even-longer"}'
{"short_url":"http://localhost:8000/shrt/aZ3kQ9x"}
```

Returns 201 for a new link, 200 if the URL was already shortened, 400 for invalid input.

Expand it back:

```
$ curl -X POST localhost:8000/api/expand/ -H 'Content-Type: application/json' \
    -d '{"short_url": "http://localhost:8000/shrt/aZ3kQ9x"}'
{"url":"http://example.com/very-very/long/url/even-longer"}
```

Returns 404 if the code doesn't exist, 400 if the input doesn't look like a short URL.

Follow it:

```
$ curl -i localhost:8000/shrt/aZ3kQ9x
HTTP/1.1 302 Found
Location: http://example.com/very-very/long/url/even-longer
```
