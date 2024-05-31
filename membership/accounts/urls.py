from django.urls import path
from . import views


urlpatterns = [
    path("<int:user_id>/addresses", views.AccountView.as_view()),
]