from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import TrackAnimeSerializer
from .models import TrackAnime
from .tasks import parse_from_tracker


# Create your views here.
class TrackAnimeAPIView(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    queryset = TrackAnime.objects.all()
    serializer_class = TrackAnimeSerializer

    permission_classes = (IsAdminUser,)

    @action(detail=False, methods=['GET'])
    def track(self, request):
        parse_from_tracker.delay()
        return Response('')
