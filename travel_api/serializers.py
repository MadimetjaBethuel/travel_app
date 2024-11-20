
from rest_framework import serializers
from .models import  activities, itinerary

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = activities
        fields = ['id', 'name', 'start_date', 'end_date', 'description', 'created_at', 'updated_at']

class ItinerarySerializer(serializers.ModelSerializer):
    activities = ActivitySerializer(many=True, read_only=True)
    class Meta:
        model = itinerary
        fields = ['id', 'destination', 'activities','start_date', 'end_date', 'weather', 'created_at', 'updated_at'] 
