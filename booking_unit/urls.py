from django.urls import path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('businesses', views.BusinessViewSet)
router.register('services', views.ServiceViewSet)
router.register('requests', views.RequestViewSet)
request_router = routers.NestedDefaultRouter(router, 'requests', lookup='request')
request_router.register('offers', views.OfferViewSet, basename='request-offers')
services_router = routers.NestedDefaultRouter(router, 'services', lookup='service')
services_router.register('reviews', views.ReviewViewSet, basename='service-reviews')
services_router.register('images', views.ServiceImageViewSet, basename='service-images')
services_router.register('videos', views.ServiceVideoViewSet, basename='service-videos')


urlpatterns = router.urls + services_router.urls + request_router.urls
urlpatterns += [
    # path('booking_page', views.booking_payment, name='booking_page'),
    # path('booking_successful', views.booking_sucessful, name='booking_successful'),
    # path('booking_cancelled', views.booking_cancelled, name='booking_cancelled'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('email/', views.send_email, name='send_email'),
]