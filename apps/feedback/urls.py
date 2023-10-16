from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet

router = DefaultRouter()

router.register('comment', CommentViewSet)
router.register('review', ReviewViewSet)

urlpatterns = router.urls
