from django.shortcuts import render
import stripe
import time
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404 
from django.core.mail import send_mail, BadHeaderError
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import (CreateBusinessSerializer, CreateServiceSerializer, ServiceImageSerializer,
                           ServiceVideoSerializer, ReviewSerializer, RequestSerializer,
                           CreateOfferSerializer, OfferSerializer, BookingSerializer)
from .models import (Business, Booking, Service, ServiceImage,
                      ServiceVideo, Payment, Review, Request, Offer)

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
    
@login_required(login_url='login')
def booking_page(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items = [
            {
                'price': 2000,
                'quantity': 1
            
            }],
            mode='payment',
            customer_creation = 'always',
            sucess_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancelled_url = settings.REDIRECT_DOMAIN +'/payment_cancelled'
        )
        return HttpResponseRedirect(checkout_session.urls, code=303)
    return render(request, 'user_payment/booking_page.html')


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user.id
    try:
        payment = Payment.objects.get(user_id=user_id)
    except Payment.DoesNotExist:
        return Response({"error": "The payment with the details does not exist"}, status=status.HTTP_404_NOT_FOUND) 
    payment.stripe_checkout_id = checkout_session_id
    payment.save()
    return render(request, 'booking_payment/payment_successful.html', {'customer': customer})


def payment_cancelled(request):
    return render('booking_payment/payment_cancelled.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    time.sleep(15)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event( 
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return Response({'error': 'could not find webhook'}, status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        return Response({'error': 'Could not verify signature'}, status=status.HTTP_400_BAD_REQUEST)
    if event['type'] == 'checkout.sesion.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        payment = Payment.objects.filter(session_id=session_id).first()
        if payment is not None:
            payment.status = 'C'
            payment.save()
        return Response(status=status.HTTP_200_OK)

@api_view()
def send_email(request):
    try:
        send_mail(subject='Booking Successful', message='Message', from_email="uniyo@gmail.com", recipient_list=["kundegodfrey3@mail.com"])
    except BadHeaderError:
        pass
    return Response("Ok")



class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}
    
    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        queryset = Booking.objects.filter(buyer=user.id)
        return queryset
    

    def destroy(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=kwargs["pk"])
        if booking.status == "S":
            return Response({"error": "Booking is cannot be deleted because it has not yet been completed"})
        return super().destroy(request, *args, **kwargs)

