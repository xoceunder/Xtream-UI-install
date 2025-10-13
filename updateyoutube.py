#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Auto-update yt-dlp (silent mode)

import os, json, urllib.request

YTDLP_PATH = "/usr/local/bin/youtube-dl"
RELEASES_URL = "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"

def get_latest_version():
    try:
        with urllib.request.urlopen(RELEASES_URL, timeout=10) as r:
            data = json.loads(r.read().decode())
            for asset in data.get("assets", []):
                if asset["name"] == "yt-dlp":
                    return asset["browser_download_url"]
    except:
        pass
    return None

def update_ytdlp(url):
    try:
        os.system(f"sudo wget -q {url} -O {YTDLP_PATH}")
        os.system(f"sudo chmod a+rx {YTDLP_PATH}")
    except:
        pass

def main():
    url = get_latest_version()
    if url:
        update_ytdlp(url)

if __name__ == "__main__":
    main()
