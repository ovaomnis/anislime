from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAdminUser

from .serializers import TrackAnimeSerializer
from .models import TrackAnime


# Create your views here.
class TrackAnimeAPIView(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    queryset = TrackAnime.objects.all()
    serializer_class = TrackAnimeSerializer
    # permission_classes = (IsAdminUser,)
