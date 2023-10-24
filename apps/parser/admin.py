from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(TrackAnime)
class TrackAnimeAdmin(admin.ModelAdmin):
    ...
