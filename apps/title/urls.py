from apps.title.views import GenreAPIView, TitleAPIView, SeasonAPIView, SeriesAPIView, RecommendationAPIView
from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('genre', GenreAPIView)
router.register('season', SeasonAPIView),
router.register('series', SeriesAPIView),
# router.register('recommendation', RecommendationAPIView)
router.register('', TitleAPIView),

urlpatterns = [
    path('recommendations/', RecommendationAPIView.as_view()),
]

urlpatterns.extend(router.urls)
