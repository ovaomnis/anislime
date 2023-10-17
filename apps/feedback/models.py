from django.contrib.auth import get_user_model
from django.db import models

from apps.title.models import Series, Title

User = get_user_model()


# Create your models here.
class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    series = models.ForeignKey(Series, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'{self.author} > {self.series}'


class Review(models.Model):
    author = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    title = models.ForeignKey(Title, related_name='reviews', on_delete=models.CASCADE)
    content = models.TextField()
