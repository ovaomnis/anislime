from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import CreatedUpdatedModelMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    slug = models.SlugField(max_length=255, primary_key=True, unique=True)
    name = models.CharField(max_length=214)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)


class TitleYear(models.Model):
    year = models.PositiveIntegerField(
        primary_key=True
    )

    def __str__(self):
        return f'{self.year}'


class Title(CreatedUpdatedModelMixin):
    slug = models.SlugField(max_length=255, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    age_rating = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(18)
    ])

    poster = models.ImageField()
    description = models.TextField()
    views = models.IntegerField(default=0)
    genres = models.ManyToManyField(Genre, related_name='titles', blank=True)
    years = models.ManyToManyField(TitleYear, related_name='titles', blank=True)
    followers = models.ManyToManyField(User, related_name='follows', blank=True)
    favourite_by = models.ManyToManyField(User, related_name='favourites', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)


class Season(models.Model):
    slug = models.SlugField(max_length=255, primary_key=True, unique=True)
    number = models.PositiveIntegerField(validators=[
        MinValueValidator(1)
    ])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'season {self.number}', allow_unicode=True)
        return super().save(*args, **kwargs)


class Series(models.Model):
    slug = models.SlugField(max_length=255, primary_key=True, unique=True)
    number = models.PositiveIntegerField(validators=[
        MinValueValidator(1)
    ])
    name = models.CharField(max_length=214)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='series')
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='series')
    video = models.FileField(upload_to='videos/')
    likes = models.ManyToManyField(User, related_name='likes')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.title.name} season {self.season.number} series {self.number}',
                                allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.slug}'
