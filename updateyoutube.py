#!/usr/bin/python3
# -*- coding: utf-8 -*-
# update panel
import subprocess, os, sys
from itertools import cycle, izip

def updateyoutube():
    os.system("sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl")
    os.system("sudo chmod a+rx /usr/local/bin/youtube-dl")
    return True

if __name__ == "__main__":
    updateyoutube()
