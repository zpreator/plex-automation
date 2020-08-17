import easyimap
import imaplib
import smtplib
import datetime
import re
import numpy as np
import os
from ConfigReader import GetUsernamePassword

# imap_ssl_host = 'imap.gmail.com'
# imap_ssl_port = 993
var = GetUsernamePassword()
username = var['username']
password = var['password']
# server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)

def FilterSubject(subject):
    """ Gets information from the subject line
    such as the type and an optional folder to sort"""
    if re.findall('video|music|audio|podcast', str(subject).lower()):
        contents = subject.split(' ')
        type_ = contents[0].lower()
        try:
            folder = contents[1].replace('/', '\\')
        except:
            folder = ''
    else:
        type_ = 'video'
        folder = ''
    return type_, folder

def GetEmails():
    imapper = easyimap.connect('imap.gmail.com', username, password)
    email_list = []
    for mail_id in imapper.listids(limit=10):
        mail = imapper.mail(mail_id)
        type_, folder = FilterSubject(mail.title)
        email = {}
        email['subject'] = mail.title
        email['type'] = type_
        email['folder'] = folder
        email['body'] = mail.body
        if 'http' in email['body']:
            url_1 = email['body'].split('http')[1]
            url_2 = url_1.replace('\r', '$')
            url = 'http' + url_2.split('$')[0]
            email['url'] = url
            email['url'] = str(url.strip('\r\n'))
        else:
            email['url'] = ''

        email['date'] = mail.date
        email['from'] = mail.return_path.replace('<','').replace('>','')
        email_list.append(email)

        print(mail.from_addr)
        # print(' ', mail.to)
        # print(' ', mail.cc)
        print(' Datetime: ', email['date'])
        print(' Subject: ', mail.title)
        # print(' Body: ', mail.body)
        print(' Extracted Url: ', email['url'])
        # print(' ', mail.attachments)
    return email_list

def SendEmail(to, subject, text):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    sent_from = username
    message = 'Subject: {}\n\n{}'.format(subject, text)
    server.sendmail(sent_from, to, message)
    server.close()