from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import CreateBusinessSerializer, CreateServiceSerializer
from .models import Business, Booking, Service

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
    queryset = Service.objects.all()

    def get_serializer_context(self):
        return {"request": self.request}
    

    def destroy(self, request, *args, **kwargs):
        if Booking.objects.filter(service_id=kwargs['pk']).count() > 0:
            return Response({"error": "Service has been booked cannot be deleted"})
        
        return super().destroy(request, *args, **kwargs)

