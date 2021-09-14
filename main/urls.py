from django.urls import path

from main.views import *

app_name = 'main'

urlpatterns = [
    path('districts', DistrictListAPI.as_view(), name='district_list'),
    path('communities', CommunityListAPI.as_view(), name='community_list'),
    path('streets', StreetListAPI.as_view(), name='street_list'),
    path('streets/<int:pk>', StreetDetailAPI.as_view(), name='street_detail'),
    path('houses', HouseListAPI.as_view(), name='house_list'),
    path('houses/<int:pk>', HouseDetailAPI.as_view(), name='house_detail'),
    path('apartments', ApartmentListAPI.as_view(), name='apartment_list'),
    path('apartments/<int:pk>', ApartmentDetailAPI.as_view(), name='apartment_detail'),
    path('suggestions', suggestions_view, name='suggestions_view'),
    path('suggestions/houses', suggestions_house_view, name='suggestions_house_view'),
]
