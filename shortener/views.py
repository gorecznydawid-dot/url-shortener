from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .codes import unique_code
from .models import ShortURL
from .serializers import ExpandSerializer, ShortenSerializer


class ShortenView(APIView):
    def post(self, request):
        serializer = ShortenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        short, created = ShortURL.objects.get_or_create(
            url=serializer.validated_data["url"], defaults={"code": unique_code}
        )
        short_url = request.build_absolute_uri(reverse("follow", args=[short.code]))
        return Response(
            {"short_url": short_url},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class ExpandView(APIView):
    def post(self, request):
        serializer = ExpandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        short = get_object_or_404(ShortURL, code=serializer.validated_data["short_url"])
        return Response({"url": short.url})


def follow(request, code):
    short = get_object_or_404(ShortURL, code=code)
    return redirect(short.url)
