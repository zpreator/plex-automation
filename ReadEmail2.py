import pytube
import subprocess
import re
from moviepy.editor import *
# folder = "E://Music//TwentyOnePilots//Trench"
# subprocess.call([                               # or subprocess.run (Python 3.5+)
#     "C:\\FFmpeg\\bin\\ffmpeg.exe",
#     '-i', "E:\\Music\\TwentyOnePilots\\Trench\\twenty one pilots - Jumpsuit (Official Video).mp4",
#     "E:\\Music\\TwentyOnePilots\\Trench\\twenty one pilots - Jumpsuit (Official Video).mp3"
# ])
# video = VideoFileClip(os.path.join(folder,"twenty one pilots - Jumpsuit (Official Video).mp4"))
# video.audio.write_audiofile(os.path.join(folder, "twenty one pilots - Jumpsuit (Official Video).mp3"))

playlist = pytube.Playlist("https://www.youtube.com/playlist?list=OLAK5uy_mWtWynXa5NeLQEJjvrmVZmmO48G4eBBWg")
# this fixes the empty playlist.videos list
playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
urls = playlist.video_urls
print(urls)