@echo off
for /f "tokens=*" %%s in (youtubeChannels.txt) do (
  echo %%s
)
pause