from django.urls import path
from .views import KakaoMapScraper, RestaurantListAPIView, RestaurantViewSet

urlpatterns = [
    path('execute/', KakaoMapScraper().scraping_view, name='scraping_view'),
    path('scraped_list/', RestaurantListAPIView.as_view(), name='restaurant_get_list'),
    path('list/', RestaurantViewSet.as_view({'get': 'list_html'}), name='restaurant_list'),
]
