from django.urls import path
from .views import *

urlpatterns = [
    path('destinations/' , destinationLiveSearchView.as_view()),
    path('weather', weatherView.as_view()),
    path('itineraries', createItineraryView.as_view()),
    path('itineraries/<str:itinerary_id>', getItineraryView.as_view()),
    path('activities/', ActivityView.as_view()),
    path('activities/<str:itinerary_id>', ActivityView.as_view()),
    path('activity/<str:activity_id>', ItineraryActivitiesView.as_view()),
]