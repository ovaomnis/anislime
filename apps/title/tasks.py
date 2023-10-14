from config.celery import app
from django.core.mail import send_mail
from django.template.loader import render_to_string


@app.task
def send_series_followers(title, emails):
    template_message = render_to_string('send_mail.html', {'title': title})

    send_mail(
        'AniSlime',
        f'Hi new series of {title} already out, come to our website and watch it!',
        'sayansenedwne@gmail.com',
        emails,
        html_message=template_message
    )
