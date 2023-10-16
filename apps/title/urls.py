from apps.title.views import GenreAPIView, TitleAPIView, SeasonAPIView, SeriesAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('genre', GenreAPIView)
router.register('season', SeasonAPIView),
router.register('series', SeriesAPIView),
router.register('', TitleAPIView),

urlpatterns = []

urlpatterns.extend(router.urls)
