import youtube_dl
import os
import datetime
import numpy as np
from Download import GetInfo

channels = np.loadtxt("C:\Repos\plex-automation\youtubeChannels.txt", dtype=str)
print(channels)

for channel in channels:
    ydl_opts = {
                'ffmpeg_location': "C:\\ffmpeg\\bin\\ffmpeg.exe",
                'format': 'bestvideo',
                'outtmpl': 'E:\\YouTube\\%(uploader)s\\%(title)s.%(id)s.%(ext)s'
            }