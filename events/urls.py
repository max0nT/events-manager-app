from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r"events", views.EventViewSet, basename="events")
router.register(r"places", views.PlaceViewSet, basename="places")

urlpatterns = router.urls
