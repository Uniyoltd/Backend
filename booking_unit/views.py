from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404 
from rest_framework import status

from .serializers import (CreateBusinessSerializer, CreateServiceSerializer, ServiceImageSerializer,
                           ServiceVideoSerializer, ReviewSerializer, RequestSerializer,
                           CreateOfferSerializer, OfferSerializer)
from .models import (Business, Booking, Service, ServiceImage,
                      ServiceVideo, Review, Request, Offer)

class BusinessViewSet(ModelViewSet):
    serializer_class = CreateBusinessSerializer
    # permission_classes = [IsAuthenticated]
    queryset = Business.objects.all()

    def get_serializer_context(self):
        return {"request": self.request}
    

    def destroy(self, request, *args, **kwargs):
        if Service.objects.filter(business_id=kwargs['pk']).count() > 0:
            return Response({"error": "Business associated to a service cannot be deleted"})
        
        return super().destroy(request, *args, **kwargs)



class ServiceViewSet(ModelViewSet):
    serializer_class = CreateServiceSerializer
    # permission_classes = [IsAuthenticated]
    queryset = Service.objects.prefetch_related('images').all()

    def get_serializer_context(self):
        return {"request": self.request}
    

    def destroy(self, request, *args, **kwargs):
        if Booking.objects.filter(service_id=kwargs['pk']).count() > 0:
            return Response({"error": "Service has been booked cannot be deleted"})
        
        return super().destroy(request, *args, **kwargs)

class ServiceImageViewSet(ModelViewSet):
    serializer_class = ServiceImageSerializer

    def get_queryset(self):
        return ServiceImage.objects.filter(service_id=self.kwargs['service_pk'])

    def get_serializer_context(self):
        return {'service_id': self.kwargs['service_pk']}
    

class ServiceVideoViewSet(ModelViewSet):
    serializer_class = ServiceVideoSerializer

    def get_queryset(self):
        return ServiceVideo.objects.filter(service_id=self.kwargs['service_pk'])

    def get_serializer_context(self):
        return {'service_id': self.kwargs['service_pk']}
    
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(service_id=self.kwargs['service_pk'])
    
    def get_serializer_context(self):
        return {'service_id': self.kwargs['service_pk']}
    

class RequestViewSet(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all()

    def get_serializer_class(self):

        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CreateOfferSerializer
        return OfferSerializer
    
    def get_serializer_context(self):
        return {'request_id': self.kwargs['request_pk']}
    
    def destroy(self, request, *args, **kwargs):
        offer = get_object_or_404(Offer, pk=kwargs.get('pk'))
        if offer.business.owner.id != self.request.user.id:
            return  Response(
                {
                    "error": "You are not authorized to delete this offer."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)