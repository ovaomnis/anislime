from rest_framework.routers import DefaultRouter

from apps.title.views import GenreAPIView, TitleAPIView, SeasonAPIView, SeriesAPIView

router = DefaultRouter()
router.register('genre', GenreAPIView)
router.register('season', SeasonAPIView),
router.register('series', SeriesAPIView),
router.register('', TitleAPIView),

urlpatterns = []

urlpatterns.extend(router.urls)
