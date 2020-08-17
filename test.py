from __future__ import unicode_literals
import youtube_dl
import os
# %(playlist)s/%(playlist_index)s - %(title)s.%(ext)s
url = 'https://www.youtube.com/playlist?list=OLAK5uy_mWtWynXa5NeLQEJjvrmVZmmO48G4eBBWg'

def Download(url, media_type):
    if 'list' in url:
        if media_type == 'audio' or media_type == 'podcast':
            base = 'E://Podcasts/'
        elif media_type == 'music':
            base = 'E://Music/'
        elif media_type == 'video':
            base = 'E://Youtube/'
    else:
        if media_type == 'audio' or media_type == 'podcast':
            ydl_opts = {
                'format': 'bestvideo',
                'forceurl': True,
                'outtmpl': 'E://YouTube/%(title)s.%(ext)s'
            }
        elif media_type == 'music':
            ydl_opts = {
                'format': 'bestvideo',
                'forceurl': True,
                'outtmpl': 'E://YouTube/%(title)s.%(ext)s'
            }
        elif media_type == 'video':
            ydl_opts = {
                'format': 'bestvideo',
                'forceurl': True,
                'outtmpl': 'E://YouTube/%(title)s.%(ext)s'
            }
    youtube_dl.utils.std_headers['User-Agent'] = "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"
    video = youtube_dl.YoutubeDL({}).extract_info(                            
    url, download=False)
    song_name = video["track"]
    artist = video["artist"]
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     video = ydl.download([url])
    #     print(video)

def Download2(youtube_url, media_type):
    if media_type == 'audio' or media_type == 'podcast':
        base = 'E://Podcasts/'
    elif media_type == 'music':
        base = 'E://Music/'
    elif media_type == 'video':
        base = 'E://Youtube/'

    infos = GetInfo(youtube_url)
    if 'list' in youtube_url:
        artist = infos[0]['playlist_uploader'].lower().title()
    else:
        artist = infos[0]['uploader']

    for info in infos:
        url = info['webpage_url']
        title = info['title']
        ext = info['ext']
        ydl_opts = {
                'format': 'bestvideo',
                'outtmpl': os.path.join(base, artist, '%(title)s.%(ext)s')
            }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if media_type != 'video':
            subprocess.call([                               # or subprocess.run (Python 3.5+)
                "C:\\FFmpeg\\bin\\ffmpeg.exe",
                '-i', os.path.join(base, artist, title + ext),
                os.path.join(base, artist, title + 'mp3')
            ])
            os.remove(os.path.join(base, artist, title + ext))

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
        return info

# Download(url, 'music')
# GetInfo(url)
Download2(url, 'music')