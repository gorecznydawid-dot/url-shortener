import pytest

from shortener import codes
from shortener.models import ShortURL


def test_generate_code_format():
    code = codes.generate_code()
    assert len(code) == 7
    assert all(c in codes.ALPHABET for c in code)


def test_generate_code_is_random():
    assert len({codes.generate_code() for _ in range(100)}) == 100


@pytest.mark.django_db
def test_unique_code_retries_on_collision(monkeypatch):
    ShortURL.objects.create(url="http://example.com", code="aaaaaaa")
    generated = iter(["aaaaaaa", "aaaaaaa", "bbbbbbb"])
    monkeypatch.setattr(codes, "generate_code", lambda: next(generated))

    assert codes.unique_code() == "bbbbbbb"


@pytest.mark.django_db
def test_unique_code_gives_up_after_max_attempts(monkeypatch):
    ShortURL.objects.create(url="http://example.com", code="aaaaaaa")
    monkeypatch.setattr(codes, "generate_code", lambda: "aaaaaaa")

    with pytest.raises(RuntimeError):
        codes.unique_code()
