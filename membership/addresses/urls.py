from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("", views.AddressView.as_view()),
    path("<int:address_id>/", views.AddressView.as_view()),

    path("getToken", obtain_auth_token),
    path("login/simpleJWT", TokenObtainPairView.as_view()),
    path("login/simpleJWT/refresh", TokenRefreshView.as_view()),
    path("login/simpleJWT/verify", TokenVerifyView.as_view()),
]