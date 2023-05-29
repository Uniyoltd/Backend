from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

class Business(models.Model):
    owner = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='business/images', null=True)
    status  = models.CharField(max_length=255)


    def get_status(self):
        return self.status
    

    def set_status(self, status):
        self.status = status



class Service(models.Model):
    name = models.CharField(max_length=255)
    business = models.ForeignKey(to=Business, on_delete=models.CASCADE, related_name='services')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    transport_per_km = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    availability = models.CharField(max_length=255)


class ServiceImage(models.Model):
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='services/images')


class ServiceVideo(models.Model):
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='services/videos')


class Request(models.Model):
    STATUS_CHOICES = [
        ('O', 'Open'),
        ('C', 'Closed')
    ]
    customer = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customers')
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='request/images', null=True)
    video = models.FileField(upload_to='request/videos', null=True)
    created_at = models.DateTimeField(auto_now=True)
    delivery_at = models.DateTimeField(null=True)
    duration_in_hours = models.FloatField(null=True)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

class Offer(models.Model):
    business = models.ForeignKey(to=Business, on_delete=models.CASCADE)
    request = models.ForeignKey(to=Request, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Booking(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('S', 'Paid'),
        ('C', 'Completed'),
    ]

    buyer = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='buyers')
    booked_at = models.DateTimeField(auto_now=True)
    delivery_at = models.DateTimeField(null=True)
    duration_in_hours = models.FloatField(null=True)
    service = models.ForeignKey(to=Service, on_delete=models.PROTECT, related_name='booked_services')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    transport_per_km = models.DecimalField(max_digits=8, decimal_places=2)
    address = models.CharField(max_length=255)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default=STATUS_CHOICES[0][0])


class Review(models.Model):
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)


class Payment(models.Model):
    PAYMENT_STATUSES = [
        ('P', 'Pending'),
        ('C', 'Completed')
    ]
    stripe_checkout_id = models.CharField(max_length=500, unique=True, null=True)
    booking = models.OneToOneField(to=Booking, on_delete=models.CASCADE, related_name='payment') 
    status = models.CharField(max_length=1, default=PAYMENT_STATUSES[0][0])
    paid_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Booking)
def create_booking_payment(sender, instance, created, **kwargs):
    if created:
        Payment.objects.create(booking=instance)