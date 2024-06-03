from django.urls import path
from posts.views import feeds

urlpatterns = [
    path("feeds/", feeds),
]