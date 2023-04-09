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