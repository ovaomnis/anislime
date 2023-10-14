from rest_framework import serializers
from .models import TrackAnime


class TrackAnimeSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = TrackAnime
        fields = "__all__"

    def validate_uri(self, uri: str):
        if uri.startswith('http://') or uri.startswith('https://'):
            raise serializers.ValidationError('starts with host. enter just uri')
        if self.Meta.model.objects.filter(uri=uri).exists():
            raise serializers.ValidationError('this uri is already tracking or parsed')
        return uri
