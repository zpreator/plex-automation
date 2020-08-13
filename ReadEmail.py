import imaplib
import datetime
import re
import numpy as np

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = 'icebergplex@gmail.com'
password = 'Oct0pu$20'
server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)

def GetEmails():
    server.login(username, password)
    server.select('INBOX')

    status, data = server.search(None, 'ALL')
    urls = []
    for num in data[0].split():
        status, data = server.fetch(num, '(RFC822)')
        email_msg = str(data[0][1])

        subject_1 = email_msg.split('Subject: ')[1]
        subject = subject_1.split(r'\r')[0]
        print('Subject: ', subject)

        time = re.findall("[\d]{1,2} [ADFJMNOS]\w* [\d]{4} [0-9][0-9]:[0-9][0-9]:[0-9][0-9]", email_msg)[0]
        datetime_ = datetime.datetime.strptime(time, '%d %b %Y %H:%M:%S')
        print('  Time: ', datetime_)
        try:
            body_1 = email_msg.split('Mailer: ')[1]
            if 'http' in body_1:
                url_1 = body_1.split('http')[1]
                url = 'http' + url_1.split(r'\r')[0]
                print('  Url: ', url)
                urls.append([url, datetime_])
        except:
            pass
    return urls

def GetPreviousTime():
    previous_time = np.loadtxt('log.txt', dtype=str)
    # var = ''
    # for i in previous_time:
    #     var += i + ' '
    # previous_datetime = datetime.datetime.strptime(str(var), '%d %b %Y %H:%M:%S ')
    previous_datetime = datetime.datetime.fromisoformat(str(previous_time))
    return previous_datetime

if __name__ == "__main__":   
    urls = GetEmails()
    print('')
    for i in range(len(urls)):
        var = urls[-1-i]
        time = var[1]
        url = var[0]
        prev_time = GetPreviousTime()
        if time > prev_time:
            print('Saving: ', url)
    iso = urls[-1][1].isoformat()
    np.savetxt('log.txt', np.array([iso]), fmt='%s')