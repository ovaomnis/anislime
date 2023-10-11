from apps.title.models import Genre, Title, Season, Series
from rest_framework import serializers


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    year = serializers.IntegerField(read_only=True)
    class Meta:
        model = Title
        fields = '__all__'

    def validate_name(self, name):
        if self.Meta.model.objects.filter(name=name).exists():
            raise serializers.ValidationError('Такой тайтл с таким именем уже существует')
        return name


class SeasonSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Season
        fields = '__all__'


class SeriesSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Series
        fields = '__all__'
