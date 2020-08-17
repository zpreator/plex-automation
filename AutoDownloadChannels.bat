cd /D "%~dp0"
@echo off
for /f "tokens=*" %%s in (youtubeChannels.txt) do (
  youtube-dl %%s --config-location autoDownloadConfig.txt
)
PAUSE