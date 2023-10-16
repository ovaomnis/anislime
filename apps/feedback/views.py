from rest_framework import viewsets, mixins

from .models import Comment, Review
from .permissions import IsAuthorOrIsAdminOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer


# Create your views here.
class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrIsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrIsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
