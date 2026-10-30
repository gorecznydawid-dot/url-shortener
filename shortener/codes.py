import secrets
import string

from .models import ShortURL

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 7
MAX_ATTEMPTS = 10


def generate_code():
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))


def unique_code():
    for _ in range(MAX_ATTEMPTS):
        code = generate_code()
        if not ShortURL.objects.filter(code=code).exists():
            return code
    raise RuntimeError("Could not generate a unique code")
