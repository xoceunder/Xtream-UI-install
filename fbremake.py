#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess, os, sys, base64, json, urllib.request
from itertools import cycle

rPlat = "https://bitbucket.org/xoceunder/xtream-ui-install/raw/main/sub_xui_xoceunder.zip"
rPackages = ["libcurl3", "libcurl4", "libxslt1-dev", "libgeoip-dev", "libonig-dev", "e2fsprogs", "wget", "mcrypt", "nscd", "htop", "zip", "unzip", "mc", "libzip5", "python", "python3-paramiko", "python-is-python3"]

initd_script = """#!/bin/sh
### BEGIN INIT INFO
# Provides:          xtreamcodes
# Required-Start:    $network $local_fs $remote_fs $time
# Required-Stop:     $network $local_fs $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Xtream Codes IPTV Panel
# Description:       Controla el servicio Xtream Codes IPTV Panel (start|stop|restart|reload)
### END INIT INFO
SCRIPT=/home/xtreamcodes/iptv_xtream_codes/xtreamcodes
NAME=xtreamcodes

case "$1" in
  start)
    $SCRIPT start
    ;;
  stop)
    $SCRIPT stop
    ;;
  restart)
    $SCRIPT restart
    ;;
  reload)
    $SCRIPT reload
    ;;
  status)
    pids=$(pgrep -u xtreamcodes nginx | wc -l)
    if [ "$pids" -gt 0 ]; then
      echo "$NAME is running"
    else
      echo "$NAME is stopped"
    fi
    ;;
  *)
    echo "Usage: /etc/init.d/$NAME {start|stop|restart|reload|status}"
    exit 1
    ;;
esac

exit 0

"""

def get_GeoLite2():
    try:
        with urllib.request.urlopen("https://api.github.com/repos/P3TERX/GeoLite.mmdb/releases/latest", timeout=10) as r:
            data = json.loads(r.read().decode())
            tag = data.get("tag_name")
            if tag:
                return f"https://github.com/P3TERX/GeoLite.mmdb/releases/download/{tag}/GeoLite2-City.mmdb"
    except: return ""

def get_youtube():
    try:
        with urllib.request.urlopen("https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest", timeout=10) as r:
            data = json.loads(r.read().decode())
            for asset in data.get("assets", []):
                if asset["name"] == "yt-dlp":
                    return asset["browser_download_url"]
    except:
        pass
    return None, None
        
def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def getVersion():
    try: return subprocess.check_output("lsb_release -d".split()).decode().strip().split(":")[-1].strip()
    except: return ""
  
def getCodename():
    try: return os.popen("lsb_release -sc").read().strip()
    except: return "" 
        
def is_installed(package_name):
    try:
        subprocess.run(['dpkg', '-s', package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def prepare():
    global rPackages
    for rFile in ["/var/lib/dpkg/lock-frontend", "/var/cache/apt/archives/lock", "/var/lib/dpkg/lock"]:
        try: os.remove(rFile)
        except: pass
    os.system("apt-get update > /dev/null")
    for rPackage in rPackages:
        if not is_installed(rPackage):
            subprocess.run(f"sudo DEBIAN_FRONTEND=noninteractive apt-get install {rPackage} -yq > /dev/null 2>&1", shell=True)
    if not is_installed("libssl1.1"):
        subprocess.run("wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.0g-2ubuntu4_amd64.deb > /dev/null 2>&1 && sudo dpkg -i libssl1.1_1.1.0g-2ubuntu4_amd64.deb > /dev/null 2>&1 && rm -rf libssl1.1_1.1.0g-2ubuntu4_amd64.deb > /dev/null 2>&1", shell=True)
    os.system("apt-get install -f > /dev/null")
    os.system("adduser --system --shell /bin/false --group --disabled-login xtreamcodes > /dev/null")
    if not os.path.exists("/home/xtreamcodes"): os.mkdir("/home/xtreamcodes")
    return True

def install():
    global rPlat
    rURL = rPlat
    rNginx = "/home/xtreamcodes/iptv_xtream_codes/nginx/conf/nginx.conf"
    rNginxRtmp = "/home/xtreamcodes/iptv_xtream_codes/nginx_rtmp/conf/nginx.conf"
    if not "xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    xtream-codes.com" >> /etc/hosts')
    if not "api.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    api.xtream-codes.com" >> /etc/hosts')
    if not "downloads.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    downloads.xtream-codes.com" >> /etc/hosts')
    if not "xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    xtream-codes.com" >> /etc/hosts')
    if not "/home/xtreamcodes/iptv_xtream_codes/" in open("/etc/fstab").read():
        rFile = open("/etc/fstab", "a")
        rFile.write("tmpfs /home/xtreamcodes/iptv_xtream_codes/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\ntmpfs /home/xtreamcodes/iptv_xtream_codes/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=2G 0 0")
        rFile.close()
    os.system('wget -q -O "/tmp/xtreamcodes.zip" "%s"' % rURL)
    if not "/sbin/iptables" in open("/etc/sudoers").read(): os.system('sed -i "s|xtreamcodes|#xtreamcodes|g" /etc/sudoers && echo "xtreamcodes ALL=(root) NOPASSWD: /sbin/iptables" >> /etc/sudoers')
    if not os.path.exists("/etc/init.d/xtreamcodes"): os.system("touch /etc/init.d/xtreamcodes")
    if not "Provides" in open("/etc/init.d/xtreamcodes").read():
        os.system("rm /etc/init.d/xtreamcodes")
        rStart = open("/etc/init.d/xtreamcodes", "w")
        rStart.write(initd_script)
        rStart.close()
        os.system("chmod 755 /etc/init.d/xtreamcodes >/dev/null 2>&1")
        os.system("update-rc.d xtreamcodes defaults >/dev/null 2>&1")
    if os.path.exists("/usr/bin/ffmpeg"):
        os.remove("/usr/bin/ffmpeg")
    if os.path.exists("/tmp/xtreamcodes.zip"):
        os.system('mv "%s" "%s.xc" && mv "%s" "%s.xc"' % (rNginx, rNginx, rNginxRtmp, rNginxRtmp))
        os.system("chattr -i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb")
        os.system("umount -l /home/xtreamcodes/iptv_xtream_codes/streams")
        os.system("umount -l /home/xtreamcodes/iptv_xtream_codes/tmp")
        os.system('unzip -o "/tmp/xtreamcodes.zip" -d "/home/xtreamcodes/" >/dev/null 2>&1')
        if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/xtreamcodes"): 
            os.system("wget -q https://github.com/xoceunder/Xtream-UI-install/raw/main/xtreamcodes -O /home/xtreamcodes/iptv_xtream_codes/xtreamcodes")
            os.system("sudo chmod +x /home/xtreamcodes/iptv_xtream_codes/xtreamcodes")
        os.system('wget -q -O "/home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb" "%s"' % get_GeoLite2())
        os.system("mount -a")
        os.system('mv "%s.xc" "%s" && mv "%s.xc" "%s"' % (rNginx, rNginx, rNginxRtmp, rNginxRtmp))
        os.system("ln -sf /home/xtreamcodes/iptv_xtream_codes/bin/ffmpeg /usr/bin/")
        os.system("rm /usr/local/bin/youtube-dl >/dev/null 2>&1")
        os.system('wget -q -O "/usr/local/bin/youtube-dl" "%s"' % get_youtube())
        os.system("chmod a+rx /usr/local/bin/youtube-dl")
    if not "www.google.com" in open("/home/xtreamcodes/iptv_xtream_codes/wwwdir/index.php").read(): os.system("sed -i 's|echo \"Xtream Codes Reborn\";|header(\"Location: https://www.google.com/\");|g' /home/xtreamcodes/iptv_xtream_codes/wwwdir/index.php >/dev/null 2>&1")
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/tv_archive"): os.mkdir("/home/xtreamcodes/iptv_xtream_codes/tv_archive/")
    os.system("mount -a")
    os.system("chown -R xtreamcodes:xtreamcodes /home/xtreamcodes")
    os.system("chmod -R 0777 /home/xtreamcodes")
    os.system("chattr +i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb")
    try: os.remove("/tmp/xtreamcodes.zip")
    except: pass
    if os.path.exists("/home/xtreamcodes/iptv_xtream_codes/start_services.sh"):
        os.remove("/home/xtreamcodes/iptv_xtream_codes/start_services.sh")
    if not "Provides" in open("/etc/init.d/xtreamcodes").read():
        os.system("rm /etc/init.d/xtreamcodes")
        rStart = open("/etc/init.d/xtreamcodes", "w")
        rStart.write(initd_script)
        rStart.close()
        os.system("chmod +x /etc/init.d/xtreamcodes")
        os.system("update-rc.d xtreamcodes defaults")
        return True
    return False

def encrypt(rHost="127.0.0.1", rUsername="user_iptvpro", rPassword="", rDatabase="xtream_iptvpro", rServerID=1, rPort=7999):
    try: os.remove("/home/xtreamcodes/iptv_xtream_codes/config")
    except: pass
    rf = open("/home/xtreamcodes/iptv_xtream_codes/config", 'wb')
    lestring=''.join(chr(ord(c)^ord(k)) for c,k in zip('{\"host\":\"%s\",\"db_user\":\"%s\",\"db_pass\":\"%s\",\"db_name\":\"%s\",\"server_id\":\"%d\", \"db_port\":\"%d\"}' % (rHost, rUsername, rPassword, rDatabase, rServerID, rPort), cycle('5709650b0d7806074842c6de575025b1')))
    rf.write(base64.b64encode(bytes(lestring, 'ascii')))
    rf.close()

def start(): 
    os.system("chown xtreamcodes:xtreamcodes /home/xtreamcodes/iptv_xtream_codes/config")
    os.system("chmod 0700 /home/xtreamcodes/iptv_xtream_codes/config")
    os.system("systemctl restart xtreamcodes")

if __name__ == "__main__":
    rHost = sys.argv[1]
    rPort = int(sys.argv[2])
    rUsername = sys.argv[3]
    rPassword = sys.argv[4]
    rDatabase = sys.argv[5]
    rServerID = int(sys.argv[6])
    prepare()
    install()
    encrypt(rHost, rUsername, rPassword, rDatabase, rServerID, rPort)
    start()
