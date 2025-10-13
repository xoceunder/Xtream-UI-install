#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Auto-update GeoLite2.mmdb using GitHub release tag (silent)

import os, json, urllib.request

GEOLITE_PATH = "/home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb"
RELEASES_URL = "https://api.github.com/repos/P3TERX/GeoLite.mmdb/releases/latest"
TMP_TAG_FILE = "/home/xtreamcodes/iptv_xtream_codes/geolite_version.txt"

def get_latest_tag():
    try:
        with urllib.request.urlopen(RELEASES_URL, timeout=10) as r:
            data = json.loads(r.read().decode())
            return data.get("tag_name", "")
    except:
        return ""

def get_stored_tag():
    try:
        with open(TMP_TAG_FILE, "r") as f:
            return f.read().strip()
    except:
        return ""

def save_tag(tag):
    try:
        with open(TMP_TAG_FILE, "w") as f:
            f.write(tag)
    except:
        pass

def update_geolite():
    latest_tag = get_latest_tag()
    if not latest_tag:
        return  # no se pudo obtener info
    stored_tag = get_stored_tag()
    # Solo actualiza si no existe o hay nueva versión
    if latest_tag == stored_tag and os.path.exists(GEOLITE_PATH):
        return
    url = f"https://github.com/P3TERX/GeoLite.mmdb/releases/download/{latest_tag}/GeoLite2-City.mmdb"
    try:
        os.system(f"sudo wget -q {url} -O {GEOLITE_PATH}")
        os.system(f"sudo chmod 644 {GEOLITE_PATH}")
        save_tag(latest_tag)
    except:
        pass

if __name__ == "__main__":
    update_geolite()
