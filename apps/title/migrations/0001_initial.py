# Generated by Django 4.2.6 on 2023-10-11 14:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='Title',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('orig_name', models.CharField(max_length=255)),
                ('age_rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(18)])),
                ('poster', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('year', models.IntegerField(default=django.utils.timezone.now)),
                ('genres', models.ManyToManyField(blank=True, related_name='titles', to='title.genre')),
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
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='series', to='title.season')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='series', to='title.title')),
            ],
        ),
    ]
