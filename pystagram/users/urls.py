from django.urls import path
from users.views import login_view, logout_view, signup

app_name = "users"
urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", signup, name="signup"),
]