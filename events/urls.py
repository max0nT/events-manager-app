from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r"events", views.EventViewSet, basename="events")
router.register(r"places", views.PlaceViewSet, basename="places")
router.register(
    r"events-export",
    views.EventExportViewSet,
    basename="events-export",
)
router.register(
    r"events-import",
    views.EventImportViewSet,
    basename="events-import",
)

urlpatterns = router.urls
