from flask import Blueprint, render_template, request, flash, redirect, url_for
from email.utils import formataddr
from email.message import EmailMessage
import smtplib

email = Blueprint('email', __name__)


@email.route('/email')

def sendmail(sub, sender, sendmail, recieve, recmail, message):

   # Create a text/plain message
   msg = EmailMessage()
   msg.set_content(message)

   # me == the sender's email address
   # you == the recipient's email address

   # msg = MIMEText(message.encode('utf-8'), _charset='utf-8')
   msg['Subject'] = sub
   msg['From'] = formataddr((sender, sendmail))
   msg['To'] = formataddr((recieve, recmail))

   server = smtplib . SMTP ( 'smtp.gmail.com' , 587 )
   server.starttls ( )
   server.login ( 'adhdestinies@gmail.com' , 'ufcjvdlrhjdbhwco')
   server.send_message( msg)
   return 'Mail sent'


# app = current_app._get_current_object()
#
# email = Blueprint('email', __name__)
# current_app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# current_app.config['MAIL_PORT'] = 465
# current_app.config['MAIL_USERNAME'] = 'adhdestinies@gmail.com'
# current_app.config['MAIL_PASSWORD'] = 'ufcjvdlrhjdbhwco'
# current_app.config['MAIL_USE_TLS'] = False
# current_app.config['MAIL_USE_SSL'] = True
# current_app.config['MAIL_DEFAULT_SENDER'] = ('Muhammad Hur', 'adhdestinies@gmail.com')
#
# def async_send_mail(app, msg):
#    with app.app_context():
#       mail.send(msg)
#
# @email.route('/email')
# def sendmail():
#    msg = Message('Hello',  recipients = ['muhammadhur514@gmail.com'])
#    msg.body = "Hello Flask message sent from Flask-Mail"
#    current_app.mail.send(msg)
#    return "Sent"