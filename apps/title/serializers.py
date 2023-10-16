from django.db.models import Q
from rest_framework import serializers

from apps.feedback.serializers import ReviewSerializer, CommentSerializer
from apps.title.models import Genre, Title, Season, Series, TitleYear


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Genre
        fields = '__all__'

    def validate_name(self, name):
        if self.Meta.model.objects.filter(name=name).exists():
            raise serializers.ValidationError('Genre already exists')
        return name


class TitleYearSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(min_value=1000, max_value=9999)

    class Meta:
        model = TitleYear
        fields = '__all__'

    def create(self, validated_data):
        title_obj, _ = TitleYear.objects.get_or_create(**validated_data)
        return title_obj


class TitleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ('name', 'poster', 'slug')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.update({
            'series': instance.series.all().count(),
            'seasons': Season.objects.filter(series__in=instance.series.all()).distinct().count(),
        })
        return rep


class TitleDetailSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ('slug', 'name', 'poster', 'age_rating', 'description', 'views', 'genres', 'years', 'reviews',)
        read_only_fields = ('years',)

    def validate_name(self, name):
        if self.Meta.model.objects.filter(name=name).exists():
            raise serializers.ValidationError('Такой тайтл с таким именем уже существует')
        return name

    def create(self, validated_data):
        request = self.context.get('request')
        years = request.data.getlist('years', [])
        instance = super().create(validated_data)
        if years:
            years_sz = TitleYearSerializer(many=True, data=[{'year': year} for year in years])
            years_sz.is_valid(raise_exception=True)
            created_years = years_sz.save()
            instance.years.add(*created_years)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.update({
            'followers': instance.followers.count(),
            'favourite_by': instance.favourite_by.count(),
            'recommendations': TitleListSerializer(
                instance=Title.objects.filter(Q(genres__in=instance.genres.all()) & ~Q(slug=instance.slug)),
                many=True).data
        })
        return rep


class SeasonSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Season
        fields = '__all__'

    def validate_number(self, number):
        if self.Meta.model.objects.filter(number=number).exists():
            raise serializers.ValidationError('Season already exists')
        return number


class SeriesDetailSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Series
        fields = '__all__'

    # def to_representation(self, instance):
    def validate(self, attrs):
        number = attrs.get('number')
        if self.Meta.model.objects.filter(number=number, title=attrs.get('title')).exists():
            raise serializers.ValidationError({'title': f'Series with number {number} already exists'})
        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.count()
        return rep


class SeriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ('slug', 'name')
