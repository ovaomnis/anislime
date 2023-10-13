from django.core.mail import send_mail
from config.celery import app


@app.task
def send_series_followers(title, emails):
    send_mail(
        'AniSlime',
        f'Hi new series of {title} already out, come to our website and watch it!',
        'sayansenedwne@gmail.com',
        emails
    )
