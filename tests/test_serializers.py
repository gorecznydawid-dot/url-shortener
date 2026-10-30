import pytest

from shortener.serializers import ExpandSerializer, ShortenSerializer


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com",
        "https://example.com/very-very/long/url/even-longer?a=1&b=2#frag",
    ],
)
def test_shorten_accepts_http_and_https(url):
    serializer = ShortenSerializer(data={"url": url})
    assert serializer.is_valid(), serializer.errors


@pytest.mark.parametrize(
    "url",
    ["", "not a url", "example.com", "ftp://example.com/file", "javascript:alert(1)"],
)
def test_shorten_rejects_invalid_urls(url):
    serializer = ShortenSerializer(data={"url": url})
    assert not serializer.is_valid()
    assert "url" in serializer.errors


def test_shorten_requires_url():
    serializer = ShortenSerializer(data={})
    assert not serializer.is_valid()


def test_shorten_rejects_too_long_url():
    serializer = ShortenSerializer(data={"url": "http://example.com/" + "a" * 2048})
    assert not serializer.is_valid()


@pytest.mark.parametrize(
    "short_url",
    [
        "http://localhost:8000/shrt/aZ3kQ9x",
        "http://localhost:8000/shrt/aZ3kQ9x/",
        "https://sho.rt/shrt/aZ3kQ9x",
    ],
)
def test_expand_extracts_code(short_url):
    serializer = ExpandSerializer(data={"short_url": short_url})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["short_url"] == "aZ3kQ9x"


@pytest.mark.parametrize(
    "short_url",
    ["", "http://localhost:8000/", "http://localhost:8000/other/aZ3kQ9x", "http://localhost:8000/shrt/a-b"],
)
def test_expand_rejects_invalid_short_urls(short_url):
    serializer = ExpandSerializer(data={"short_url": short_url})
    assert not serializer.is_valid()
