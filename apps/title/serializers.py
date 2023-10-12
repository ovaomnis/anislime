from apps.title.models import Genre, Title, Season, Series, TitleYear
from rest_framework import serializers


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Genre
        fields = '__all__'


class TitleYearSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(min_value=1000, max_value=9999)

    class Meta:
        model = TitleYear
        fields = '__all__'

    def create(self, validated_data):
        title_obj, _ = TitleYear.objects.get_or_create(**validated_data)
        return title_obj


class TitleSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('years', )

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
