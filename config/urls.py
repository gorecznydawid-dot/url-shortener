from django.urls import path, re_path

from shortener import views

urlpatterns = [
    path("api/shorten/", views.ShortenView.as_view(), name="shorten"),
    path("api/expand/", views.ExpandView.as_view(), name="expand"),
    re_path(r"^shrt/(?P<code>[A-Za-z0-9]+)/?$", views.follow, name="follow"),
]
