from django.urls import path
from apps.location import views

urlpatterns = [
    # class based views
    path('countries', views.CountryList.as_view()),
    path('countries/<int:pk>', views.CountryDetail.as_view()),
    path('locations', views.LocationList.as_view()),
    path('locations/<int:pk>', views.LocationDetail.as_view()),
    path('ratings', views.RatingList.as_view()),

    # function based views
    # path('countries', views.country_list),
    # path('countries/<int:pk>', views.country_detail),
    # path('locations', views.location_list),
    # path('locations/<int:pk>', views.location_detail),

]
