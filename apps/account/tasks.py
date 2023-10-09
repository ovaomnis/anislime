from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from config.celery import app

from django.core.mail import EmailMultiAlternatives
from config.celery import app

@app.task
def send_activation_email(email, code, host):
    template = render_to_string('account/activation_code.html',
                                context={
                                    'link': host + reverse('account_activate',
                                                           kwargs={
                                                               'code': code})})
    body = strip_tags(template)

    message = EmailMultiAlternatives(
        subject='Welcome to AniSlime Family! [Account Activation Here]',
        from_email=None,
        body=body,
        to=[email]
    )
    message.attach_alternative(template, 'text/html')
    message.send()


@app.task
def send_recovery_password_code(email, code):
    template = render_to_string('account/recovery_code.html',
                                context={
                                    'code': code})
    body = strip_tags(template)

    message = EmailMultiAlternatives(
        subject='Recovery code! [AniSlime]',
        from_email=None,
        body=body,
        to=[email]
    )
    message.attach_alternative(template, 'text/html')
    message.send()
