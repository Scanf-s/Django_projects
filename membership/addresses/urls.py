from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("", views.AddressView.as_view(), name="address-list"),
    path("<int:address_id>/", views.AddressView.as_view(), name="address-detail"),

    path("getToken", obtain_auth_token, name="get-token"),
    path("login/simpleJWT", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/simpleJWT/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/simpleJWT/verify", TokenVerifyView.as_view(), name="token_verify"),
]

# 689b0059dd3d98ed58ad95444f0098727d2cab12
# "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxOTIyMjMyMiwiaWF0IjoxNzE4MDEyNzIyLCJqdGkiOiJjZTZkNGQ1NjkxNTc0YjkzOGI0OGQxZTE1Y2Y4N2JiYyIsInVzZXJfaWQiOjF9.bAXwXTItd6-JF6OrFLhN4Wj93L_qcaD8pS7_qvEcUz4",
# "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE4MDE2MzIyLCJpYXQiOjE3MTgwMTI3MjIsImp0aSI6ImQ1Mjc2YTJlZTMyOTQ2YzdiYzQ0YWU3MzM4MTBmZmEzIiwidXNlcl9pZCI6MX0.nx2tHsRSXd8tMMA6uRtQEql2KrTuYgEVUe_oNhYihCk"