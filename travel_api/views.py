from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from opencage.geocoder import OpenCageGeocode
import openmeteo_requests
import requests_cache
import requests
import os
from retry_requests import retry
from .models import itinerary,activities
from .serializers import ItinerarySerializer, ActivitySerializer
from django.db.models import F

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries= 5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

key= os.environ.get("GEO_KEY")

geolocator = OpenCageGeocode(key)
class destinationLiveSearchView(APIView):
    def get(self, request):

        """
        idea is to stream a list of destinations based on the search query 
        """

        try:

            query = request.GET.get('query')
            if query:
                results = geolocator.geocode(query)

                print(results)

                destinations = []
                if not results:
                    return Response({"message:": "No results found", "destinations":[]}, status=status.HTTP_204_NO_CONTENT)
                for result in results:
                    destination= {
                        'name': result['formatted'],
                        'lat': result['geometry']['lat'],
                        'lon': result['geometry']['lng'],
                        'country': result['components']['country'],
                        'flag': result['annotations']['flag']
                    }
                    destinations.append(destination)
                return Response({"destinations": destinations}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({"message:": e}, status=status.HTTP_400_BAD_REQUEST)
        


class weatherView(APIView):

    def post(self, request):
        """
        this should show the weather for a given location and user should decide if they want to create an itinary for the location
        
        """
        url = 'https://api.open-meteo.com/v1/forecast'
        weather_input = request.data

        if 'latitude' not in weather_input and 'longitude' not in weather_input:
            return Response({"message": "Latitude and Longitude are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            weather_info = requests.post(url, data=weather_input).json()

            return Response({"weather": weather_info}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)

        


class createItineraryView(APIView):
    def get(self, request):
        try:
            itineraries = itinerary.objects.all()
            serializer = ItinerarySerializer(itineraries, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except itinerary.DoesNotExist:
            return Response({'error': 'Itinerary not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        this should create an itinerary for a given location and user should decide if they want to create an itinary for the location
        
        """

        try:
            serializer = ItinerarySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Itinerary created successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)    
        except Exception as e:
            print(e)
            return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class getItineraryView(APIView):
    def get(self, request, itinerary_id):
        try:
            schedule = itinerary.objects.get(id=itinerary_id)
            serializer = ItinerarySerializer(schedule).data
            return Response({"itinerary": serializer}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, itinerary_id):

        try:
            schedule = itinerary.objects.get(id=itinerary_id)
            serializer = ItinerarySerializer(schedule, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Itinerary updated successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)    
        except Exception as e:
            print(e)
            return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, itinerary_id):
        print(itinerary_id)

        try:
            schedule = itinerary.objects.get(id=itinerary_id)
            schedule.delete()
            return Response({"message": "Itinerary deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)
class ActivityView(APIView):
    def get(self, request, itinerary_id):
        print('hello')
        try:
            schedule = itinerary.objects.prefetch_related('activities').get(id=itinerary_id)
            to_do_activities = schedule.activities.all()
            serializer = ActivitySerializer(to_do_activities, many=True).data
            return Response({"activities": serializer}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, itinerary_id):
        try:
            schedule = itinerary.objects.get(id=itinerary_id)
            activity = request.data
            serializer = ActivitySerializer(data=activity)
            if serializer.is_valid():
                saved_activity = serializer.save()
                schedule.activities.add(saved_activity)
                return Response({"message": "Activity created successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)    
        

class ItineraryActivitiesView(APIView):
    
    
    def put(self, request,activity_id ):
        try:
            request_data = request.data
            activity = activities.objects.get(id=activity_id)
            serializer = ActivitySerializer(activity, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Activity updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, activity_id):
        try:
            if not activity_id:
                return Response({"message": "activity_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            activity = activities.objects.get(id=activity_id)
            itineraries = itinerary.objects.filter(activities=activity)
            for itinerary_obj in itineraries:
                itinerary_obj.activities.remove(activity)
            activity.delete()
            return Response({"message": "Activity deleted successfully"}, status=status.HTTP_200_OK)
        except activities.DoesNotExist:
            return Response({"message": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
