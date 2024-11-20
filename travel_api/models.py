from django.db import models
import uuid
# Create your models here.

class activities(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False) # should use uuid
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(max_length=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  

class itinerary(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False ) # should use uuid
    destination = models.JSONField(max_length=100, blank=True, null=True)
    weather = models.JSONField( blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    activities = models.ManyToManyField(activities, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


