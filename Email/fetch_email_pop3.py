#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fetch_email_pop3.py
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

import getpass
import imaplib
import pprint

GOOGLE_IMAP_SERVER = 'imap.googlemail.com'
IMAP_SERVER_PORT = '993'

def check_email(username, password):
    mailbox = imaplib.IMAP4_SSL(GOOGLE_IMAP_SERVER, IMAP_SERVER_PORT)
    mailbox.login(username,password)
    mailbox.select('Inbox')
    tmp, data = mailbox.search(None, 'ALL')
    for num in data[0].split():
        tmp, data = mailbox.fetch(num, '(RFC822)')
        print('Message: {}\n',format(num))
        pprint.pprint(data[0][1])
    mailbox.close()
    mailbox.logout()
    

if __name__ == '__main__':
    username = input("Enter your email user ID: ")
    password = getpass.getpass(prompt = "Enter your email password: ")
    check_email(username, password)
