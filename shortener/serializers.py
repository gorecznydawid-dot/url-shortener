import re
from urllib.parse import urlparse

from rest_framework import serializers

SHORT_PATH = re.compile(r"^/shrt/([A-Za-z0-9]+)/?$")


class ShortenSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=2048)

    def validate_url(self, value):
        if urlparse(value).scheme not in ("http", "https"):
            raise serializers.ValidationError("Only http and https URLs are allowed.")
        return value


class ExpandSerializer(serializers.Serializer):
    short_url = serializers.CharField(max_length=2048)

    def validate_short_url(self, value):
        match = SHORT_PATH.match(urlparse(value).path)
        if not match:
            raise serializers.ValidationError("Not a valid short URL.")
        return match.group(1)
