from app import mail
from app import app
from .decorators import async
from flask.ext.mail import Message
from config import ADMINS
from flask import render_template

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, sender=ADMINS[0], recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)

def send_registration_email(user):
    send_email("Lavapp registration", [user.email],
            render_template("registration_email.txt", user=user), 
            render_template("registration_email.html", user=user))
