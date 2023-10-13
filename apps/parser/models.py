from django.db import models
from .utils import slugify_uri


# Create your models here.
class TrackAnime(models.Model):
    slug = models.SlugField(primary_key=True, max_length=255)
    uri = models.CharField(max_length=255)
    repeat = models.BooleanField(default=False)

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify_uri(self.uri)
        return super().save(**kwargs)
