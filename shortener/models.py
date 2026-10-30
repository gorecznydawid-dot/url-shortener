from django.db import models


class ShortURL(models.Model):
    url = models.URLField(max_length=2048, unique=True)
    code = models.CharField(max_length=16, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} -> {self.url}"
