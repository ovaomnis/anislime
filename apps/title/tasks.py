from config.celery import app
from django.core.mail import send_mail
from django.template.loader import render_to_string


@app.task
def send_series_followers(title, emails):

    send_mail(
        subject='AniSlime',
        message=f'Hi new series of {title} already out, come to our website and watch it!',
        from_email='sayansenedwne@gmail.com',
        recipient_list=emails,
    )
