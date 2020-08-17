from __future__ import unicode_literals
import easyimap
import imaplib
import smtplib
import datetime
import re
import numpy as np
import os
import pytube
import subprocess
import youtube_dl
import time

VIDEO_PATH = "E:\\YouTube"
AUDIO_PATH = "E:\\Podcasts"
MUSIC_PATH = "E:\\Music"

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = 'icebergplex@gmail.com'
password = 'Oct0pu$20'
server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)

def GetSubject2(subject):
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

def GetSubject(email_msg, this_email):
    if 'Subject' in email_msg:
        subject_1 = email_msg.split('Subject: ')[1]
        subject = subject_1.split(r'\r')[0]
        print(subject)
        this_email['subject'] = subject
        if re.findall('video|music|audio|podcast', subject.lower()):
            contents = subject.split(' ')
            this_email['type'] = contents[0].lower()
            try:
                this_email['folder'] = contents[1]
            except:
                this_email['folder'] = ''
        else:
            this_email['type'] = 'video'
            this_email['folder'] = ''
    else:
        this_email['subject'] = ''
        this_email['type'] = 'video'
        this_email['folder'] = ''
    return this_email

def GetEmails2():
    imapper = easyimap.connect('imap.gmail.com', username, password)
    email_list = []
    for mail_id in imapper.listids(limit=10):
        mail = imapper.mail(mail_id)
        type_, folder = GetSubject2(mail.title)
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

def GetEmails():
    server.login(username, password)
    server.select('INBOX')

    status, data = server.search(None, 'ALL')
    email_list = []
    for num in data[0].split():
        status, data = server.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT DATE FROM TO)])')
        status, body_data = server.fetch(num, '(RFC822)')
        email_msg = str(data[0][1])
        body = str(body_data[0][1])
        this_email = {}
        
        GetSubject(email_msg, this_email)
        
        if 'Date' in email_msg:
            date_1 = email_msg.split('Date: ')[1]
            date = date_1.split(r'\r')[0]
            print(' ', date)
            this_email['date'] = date

        if 'Mailer' in body:
            mailer_1 = body.split('Mailer: ')[1]
            if 'http' in mailer_1:
                url_1 = mailer_1.split('http')[1]
                url = 'http' + url_1.split(r'\r')[0]
                print(' ', url)
                this_email['url'] = url
            else:
                this_email['url'] = ''
        else:
            this_email['url'] = ''

        if 'From' in email_msg:
            from_1 = email_msg.split('From: ')[1]
            from_ = from_1.split(r'\r')[0]
            from_email = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", from_)[0]
            print(' ', from_email)
            this_email['from'] = from_email

        time = re.findall("[\d]{1,2} [ADFJMNOS]\w* [\d]{4} [0-9][0-9]:[0-9][0-9]:[0-9][0-9]", email_msg)[0]
        datetime_ = datetime.datetime.strptime(time, '%d %b %Y %H:%M:%S')
        print('  Time: ', datetime_)
        this_email['datetime'] = datetime_
        email_list.append(this_email)
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

def GetPreviousTime():
    previous_time = np.loadtxt("C:\\Repos\\plex-automation\\log.txt", dtype=str)
    previous_datetime = datetime.datetime.fromisoformat(str(previous_time))
    return previous_datetime

def GetCurrentTime(date):
    time = re.findall("[\d]{1,2} [ADFJMNOS]\w* [\d]{4} [0-9][0-9]:[0-9][0-9]:[0-9][0-9]", date)[0]
    datetime_ = datetime.datetime.strptime(time, '%d %b %Y %H:%M:%S')
    return datetime_

def SaveVideos(url, folder):
    import youtubeDL as dl
    if 'list=' in url:
        print(url, ' is a playlist, extracting videos..')
        dl.main(url, folder) # Playlist downloader
    else:
        yt= pytube.YouTube(url)
        yt.streams.get_highest_resolution().download(folder)

def SaveAudio(urls, folder):
    """ Saves audio tracks from youtube videos"""
    for i in urls:
        yt = pytube.YouTube(i)
        yt.streams.get_audio_only().download(folder)
        title = yt.streams.get_audio_only().default_filename
        title2 = os.path.splitext(title)[0] + '.mp3'
        subprocess.call([                               # or subprocess.run (Python 3.5+)
            "C:\\ffmpeg\\bin\\ffmpeg.exe",
            '-i', os.path.join(folder, title),
            os.path.join(folder, title2.replace(' [OFFICIAL VIDEO]', '').replace(' (Audio)', '').replace(' (Official Audio)', ''))
        ])
        os.remove(os.path.join(folder, title))

def Download(youtube_url, media_type):
    if media_type == 'audio' or media_type == 'podcast':
        base = AUDIO_PATH
    elif media_type == 'music':
        base = MUSIC_PATH
    elif media_type == 'video':
        base = VIDEO_PATH

    infos = GetInfo(youtube_url)
    if 'list' in youtube_url:
        artist = infos[0]['playlist_uploader'].lower().title()
        album = infos[0]['playlist_title']
    else:
        artist = infos[0]['uploader']
        album = 'Other'

    if media_type != 'video':
            SaveAudio([i['webpage_url'] for i in infos], os.path.join(base, artist, album))
    else:
        for info in infos:
            url = info['webpage_url']
            title = info['title'].replace(':', '#')
            ext = info['ext'].replace('webm', 'mp4')
            file_path = os.path.join(base, artist, title + '.' + ext)
            
            ydl_opts = {
                    'ffmpeg_location': "C:\\ffmpeg\\bin\\ffmpeg.exe",
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                    'outtmpl': file_path
                }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            

def GetInfo(playlist_url):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s', 'quiet':True,})
    video = ""
    info = []
    with ydl:
        result = ydl.extract_info \
        (playlist_url,
        download=False) #We just want to extract the info

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries']

            #loops entries to grab each video_url
            for i, item in enumerate(video):
                video = result['entries'][i]
                info.append(result['entries'][i])
        else:
            info.append(result)
        return info

def Save(email):
    try:
        Download(email['url'], email['type'])
        # if email['type'] == 'video':
        #     save_path = os.path.join(VIDEO_PATH, email['folder'])
        #     SaveVideos(email['url'], save_path)
        # elif email['type'] == 'music':
        #     save_path = os.path.join(MUSIC_PATH, email['folder'])
        #     SaveAudio(email['url'], save_path)
        # else:
        #     save_path = os.path.join(AUDIO_PATH, email['folder'])
        #     SaveAudio(email['url'], save_path)
        # return True
    except Exception as e:
        SendEmail(email['from'], email['subject'], 'Something went wrong while downloading the '+ email['type']+ ' file: '+ email['url'] +
        'The error was: ' + str(e))
        return False


if __name__ == "__main__": 
    email_list = GetEmails2()
    print('')
    return_list = []
    for email in email_list:
        prev_time = GetPreviousTime()
        time = GetCurrentTime(email['date'])
        if time > prev_time: # Checks to only download recent youtube videos
            print('Saving: ', email['url'])
            success = Save(email)
            if success: return_list.append(email)
    iso = GetCurrentTime(email_list[0]['date']).isoformat() # Gets most recent url
    np.savetxt("C:\\Repos\\plex-automation\\log.txt", np.array([iso]), fmt='%s') # Saves most recent url date
    for email in return_list:
        SendEmail(email['from'], email['subject'], 'Your youtube video is finished downloading!\n' +
        'Now you can watch without ads, and download to your device:)\n\n' +
        'Enjoy!\n\n\n please do not respond to this email')