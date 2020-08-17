from Email import GetEmails, SendEmail
from Time import SetCurrentTime, GetPreviousTime, GetCurrentTime
from Download import Download

def Save(email):
    """ Saves the youtube videos and handles errors"""
    try:
        Download(email)
    except Exception as e:
        SendEmail(email['from'], email['subject'], 'Something went wrong while downloading the '+ email['type']+ ' file: '+ email['url'] +
        '\n\nThe error was: ' + str(e))
        return False

if __name__ == "__main__": 
    email_list = GetEmails()
    print('')
    return_list = []
    for email in email_list:
        prev_time = GetPreviousTime()
        time = GetCurrentTime(email['date'])
        if time > prev_time: # Checks to only download recent youtube videos
            print('Saving: ', email['url'])
            success = Save(email)
            if success: return_list.append(email)
    SetCurrentTime(email_list[0]['date']) # The most recent video request
    for email in return_list:
        if email['type'] == 'video':
            message = 'Your youtube video is finished downloading!\n Now you can watch without ads, and download to your device:)\n\n'
        elif email['type'] == 'audio' or email['type'] == 'podcast':
            message = 'Your audio file is finished downloading!\n Now you can listen without ads, and download to your device:)\n\n'
        elif email['type'] == 'music':
            message = 'Your music files are finished downloading!\n Now you can listen without ads, and download to your device:)\n\n'
        SendEmail(email['from'], email['subject'], message +
                'Enjoy!\n\n\n please do not respond to this email')
