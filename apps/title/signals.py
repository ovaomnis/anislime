from apps.title.tasks import send_series_followers
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Series


@receiver(post_save, sender=Series)
def post_save_series_signal(sender, instance, created, **kwargs):
    if created:
        emails = [i.get('email') for i in instance.title.followers.all().values('email')]
        title_name = instance.title.name
        send_series_followers.delay(title_name, emails)
