from rest_framework.routers import DefaultRouter

from .views import TrackAnimeAPIView

router = DefaultRouter()
router.register('track-anime', TrackAnimeAPIView)

urlpatterns = router.urls
