from django.urls import path
from . import views


urlpatterns = [
    path("", views.AddressView.as_view()),
    path("<int:address_id>", views.AddressView.as_view())
]