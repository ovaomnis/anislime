# Generated by Django 4.2.6 on 2023-10-14 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('title', '0002_alter_title_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='is_film',
            field=models.BooleanField(default=False),
        ),
    ]
