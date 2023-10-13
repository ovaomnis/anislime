# Generated by Django 4.2.6 on 2023-10-13 08:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('slug', models.SlugField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=214)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('slug', models.SlugField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='TitleYear',
            fields=[
                ('year', models.PositiveIntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('age_rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(18)])),
                ('poster', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('views', models.IntegerField(default=0)),
                ('favourite_by', models.ManyToManyField(blank=True, related_name='favourites', to=settings.AUTH_USER_MODEL)),
                ('followers', models.ManyToManyField(blank=True, related_name='follows', to=settings.AUTH_USER_MODEL)),
                ('genres', models.ManyToManyField(blank=True, related_name='titles', to='title.genre')),
                ('years', models.ManyToManyField(blank=True, related_name='titles', to='title.titleyear')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('slug', models.SlugField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('name', models.CharField(max_length=214)),
                ('video', models.FileField(upload_to='videos/')),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='series', to='title.season')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='series', to='title.title')),
            ],
        ),
    ]
