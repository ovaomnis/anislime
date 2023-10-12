from rest_framework.response import Response
from rest_framework.decorators import action
from apps.title.models import Genre, Title, Season, Series
from apps.title.serializers import GenreSerializer, TitleDetailSerializer, SeasonSerializer, SeriesSerializer, \
    TitleListSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class GenreAPIView(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly,]


class TitleAPIView(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleDetailSerializer

    # permission_classes = [IsAuthenticatedOrReadOnly,]

    def get_serializer_class(self):
        if self.action == 'list':
            self.serializer_class = TitleListSerializer
        return super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj)
        obj.views += 1
        obj.save(update_fields=['views'])
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def follow(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.followers.filter(email=self.request.user.email).exists():
            obj.followers.remove(request.user)
            return Response('unfollowed')
        else:
            obj.followers.add(request.user)
            return Response('followed')

    @action(detail=True, methods=['post'])
    def add_favourite(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.favourite_by.filter(email=self.request.user.email).exists():
            obj.favourite_by.remove(request.user)
            return Response('removed from favourites')
        else:
            obj.favourite_by.add(request.user)
            return Response('added to favourites')

    def get_permissions(self):
        if self.action == 'follow':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class SeasonAPIView(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly,]


class SeriesAPIView(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly,]
