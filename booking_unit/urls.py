from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('businesses', views.BusinessViewSet)
router.register('services', views.ServiceViewSet)


urlpatterns = router.urls