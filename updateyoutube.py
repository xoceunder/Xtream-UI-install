#!/usr/bin/python3
# -*- coding: utf-8 -*-
# update panel
import subprocess, os

def updateyoutube():
    os.system("sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/youtube-dl")
    os.system("sudo chmod a+rx /usr/local/bin/youtube-dl")
    return True

if __name__ == "__main__":
    updateyoutube()
