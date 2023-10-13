from config.celery import app

from .models import TrackAnime
from .parser import ParseSeasonSeries


@app.task
def parse_from_tracker():
    queryset = TrackAnime.objects.all()
    for anime in queryset:
        ParseSeasonSeries(anime.uri, anime.repeat)
