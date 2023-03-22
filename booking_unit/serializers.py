from rest_framework import serializers

from .models import Business, Service, ServiceImage, ServiceVideo, Review


class ServiceImageSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        service_id = self.context['service_id']
        return ServiceImage.objects.create(service_id=service_id, **validated_data)
    

    class Meta:
        model = ServiceImage
        fields = ['id', 'image']


class ServiceVideoSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        service_id = self.context['service_id']
        return ServiceVideo.objects.create(service_id=service_id, **validated_data)
    
    class Meta:
        model = ServiceVideo
        fields = ['id', 'video']

class CreateBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [ 'owner_id', 'name', 'email', 'phone_number', 'address', 'description', 'picture']



class CreateServiceSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)
    class Meta:
        model = Service
        fields = ['id','business', 'name', 'description', 'availability', 'price', 'transport_per_km', 'images']
        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'service_id', 'name', 'description', 'date']