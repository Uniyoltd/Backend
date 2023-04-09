from rest_framework import serializers

from .models import (Business, Service, ServiceImage, 
                     ServiceVideo, Review, Request, Offer)




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

class ReviewSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        service_id = self.context['service_id']
        return Review.objects.create(service_id=service_id, **validated_data)


    class Meta:
        model = Review
        fields = ['id', 'service_id', 'name', 'description', 'date']

class CreateBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [ 'id', 'owner', 'name', 'email', 'phone_number', 'address', 'description', 'image']


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['id', 'owner', 'name', 'description', 'image', 'address']



class CreateServiceSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)
    videos = ServiceVideoSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Service
        fields = ['id','business', 'name', 'description', 'availability', 'price', 'transport_per_km', 'images', 'videos', 'reviews']
        

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['customer', 'title','image', 'video', 'price', 'created_at', 'delivery_at', 'status', 'description', 'duration_in_hours', ]

class CreateOfferSerializer(serializers.ModelSerializer):
    business_id = serializers.IntegerField()
    class Meta:
        model = Offer
        fields = ['id', 'business_id', 'description', 'price']


    def create(self, validated_data):
        request_id = self.context.get('request_id')
        return Offer.objects.create(request_id=request_id, **validated_data)


class OfferSerializer(serializers.ModelSerializer):
    request = RequestSerializer()
    business = BusinessSerializer()

    class Meta:
        model = Offer
        fields = ['id', 'request', 'business', 'description', 'price']
        
