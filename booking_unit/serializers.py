from rest_framework import serializers

from .models import Business, Service

class CreateBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [ 'id', 'name', 'email', 'phone_number', 'address', 'description', 'picture']



class CreateServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'availability', 'price', 'transport_per_km']
        