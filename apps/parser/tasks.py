from config.celery import app

from .models import TrackAnime
from .parser import ParseSeasonSeries


@app.task
def parse_from_tracker():
    queryset = TrackAnime.objects.filter(parsed=False)
    for anime in queryset:
        ParseSeasonSeries(anime.uri, anime.repeat)
        if not anime.repeat:
            anime.parsed = True
            anime.save()
