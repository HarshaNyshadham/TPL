from flask_mail import Message
from flask import render_template
from models.user import User
from flask import mail

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    msg = Message('[TPL] Reset Your Password',
                  sender='noreply@tpl.com',
                  recipients=[user.email])
    msg.body = render_template('auth/email/reset_password.txt', user=user, token=token)
    msg.html = render_template('auth/email/reset_password.html', user=user, token=token)
    mail.send(msg)