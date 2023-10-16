from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.title.models import Genre, Title, Season, Series
from apps.title.serializers import GenreSerializer, TitleDetailSerializer, SeasonSerializer, TitleListSerializer
from apps.title.serializers import SeriesDetailSerializer, SeriesListSerializer
from .permissions import IsAdminOrReadOnlyPermission


class GenreAPIView(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnlyPermission, ]


class TitleAPIView(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleDetailSerializer
    permission_classes = [IsAdminOrReadOnlyPermission, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['genres', 'age_rating', 'years']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'views']

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

    @action(detail=True, methods=['get'])
    def series(self, request, *args, **kwargs):
        obj = self.get_object()
        data = {}
        for series in obj.series.all():
            if not data.get(series.season.slug, None):
                data.update({
                    series.season.slug: [SeriesListSerializer(series).data]
                })
            else:
                data[series.season.slug].append(SeriesListSerializer(series).data)
        return Response(data)

    @action(detail=False, methods=['GET'])
    def my_follows(self, request, *args, **kwargs):
        serializer = TitleListSerializer(request.user.follows.all(), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def my_favorites(self, request, *args, **kwargs):
        serializer = TitleListSerializer(request.user.favourites.all(), many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ('follow', 'add_favourite', 'my_follows', 'my_favorites',):
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class SeasonAPIView(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

    permission_classes = [IsAdminOrReadOnlyPermission, ]


class SeriesAPIView(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesDetailSerializer
    permission_classes = [IsAdminOrReadOnlyPermission, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']

    @action(detail=True, methods=['POST'])
    def like(self, reqeust, pk):
        series_obj = self.get_object()
        like = series_obj.likes.filter(email=reqeust.user.email)
        if like:
            series_obj.likes.remove(like[0])
            return Response('unlike')
        else:
            series_obj.likes.add(self.request.user)
            return Response('like')

    def get_permissions(self):
        if self.action == 'like':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            self.serializer_class = SeriesListSerializer
        return super().get_serializer_class()
