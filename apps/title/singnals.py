from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Series


@receiver(post_save, sender=Series)
def post_save_product_signal(sender, instance, created, **kwargs):
    if created:
        print(instance.title.followers.all())
