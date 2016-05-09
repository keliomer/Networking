#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  smtp_sender.py
#  
#  Copyright 2016 Keliomer Castillo <keliomer@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import smtplib

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = 'aspmx.l.google.com'
SMTP_PORT = 25

def send_email(sender, recipient):
    """Send email message"""
    msg = MIMEMultipart()
    msg['To'] = recipient
    msg['From'] = sender
    subject = input('Enter your email subject:')
    msg['Subject'] = subject
    message = input('Enter your email message. Press enter when finished. ')
    part = MIMEText('text', "plain")
    part.set_payload(message)
    msg.attach(part)
    # create smtp session
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout = 60)
    session.ehlo()
    # session.set_debuglevel(1)
    # send mail
    session.sendmail(sender, recipient, msg.as_string())
    print("Your email is sent to {}.".format(recipient))
    session.quit()
    


if __name__ == '__main__':
    sender = input("Enter sender email address: ")
    recipient = input("Enter recipient email address: ")
    send_email(sender, recipient)
