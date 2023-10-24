from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(TitleYear)
class TitleYearAdmin(admin.ModelAdmin):
    pass


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    pass


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    pass


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    pass
