import pytube
import youtube_dl
import os
import subprocess

VIDEO_PATH = "C:\\YouTube"
AUDIO_PATH = "C:\\Podcasts"
MUSIC_PATH = "C:\\Music"

def SaveAudio(videos, base, artist):
    """ Saves audio tracks from youtube videos"""
    for video in videos:
        url = video['webpage_url']
        title = video['title']
        ext = 'mp3'
        album = video['playlist']
        file_path = os.path.join(base, artist, album, title + '.' + ext)
        ydl_opts = {
                'ffmpeg_location': "C:\\ffmpeg\\bin\\ffmpeg.exe",
                'format': 'bestaudio',
                'outtmpl': file_path
            }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def SaveVideo(videos, base, artist):
    for video in videos:
        url = video['webpage_url']
        title = video['title']
        ext = video['ext'].replace('webm', 'mp4')
        file_path = os.path.join(base, artist, title + '.' + ext)
        
        ydl_opts = {
                'ffmpeg_location': "C:\\ffmpeg\\bin\\ffmpeg.exe",
                'format': 'bestvideo',
                'outtmpl': file_path
            }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def Download(batch):
    youtube_url = batch['url']
    media_type = batch['type']
    videos = GetInfo(youtube_url)

    if 'list' in youtube_url:
        artist = videos[0]['playlist_uploader'].lower().title()
    else:
        artist = videos[0]['uploader'].lower().title()

    if media_type == 'audio' or media_type == 'podcast':
        SaveAudio(videos, AUDIO_PATH, artist)
    elif media_type == 'music':
        SaveAudio(videos, MUSIC_PATH, artist)
    elif media_type == 'video':
        SaveVideo(videos, VIDEO_PATH, artist)
            
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