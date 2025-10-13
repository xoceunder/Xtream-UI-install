#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Auto-update youtube-dl (silent, only if missing or outdated)

import os, json, urllib.request, subprocess

YTDLP_PATH = "/usr/local/bin/youtube-dl"
RELEASES_URL = "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"

def get_local_version():
    try:
        return subprocess.check_output([YTDLP_PATH, "--version"], text=True).strip()
    except:
        return None

def get_latest_version():
    try:
        with urllib.request.urlopen(RELEASES_URL, timeout=10) as r:
            data = json.loads(r.read().decode())
            version = data.get("tag_name", "").lstrip("v")
            for asset in data.get("assets", []):
                if asset["name"] == "yt-dlp":
                    return version, asset["browser_download_url"]
    except:
        pass
    return None, None

def update_ytdlp(url):
    try:
        os.system(f"sudo wget -q {url} -O {YTDLP_PATH}")
        os.system(f"sudo chmod a+rx {YTDLP_PATH}")
    except:
        pass

def main():
    local_ver = get_local_version()
    latest_ver, url = get_latest_version()
    if not url:
        return  # Could not get release info
    if local_ver != latest_ver:
        update_ytdlp(url)

if __name__ == "__main__":
    main()
