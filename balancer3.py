#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess, os, random, string, sys, shutil, socket, zipfile, urllib.request, urllib.error, urllib.parse, json, base64
from itertools import cycle
from zipfile import ZipFile
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

rDownloadURL = "https://bitbucket.org/xoceunder/xtream-ui-install/raw/main/sub_xui_xoceunder.zip"
rPackages = ["libcurl4", "libxslt1-dev", "libgeoip-dev", "e2fsprogs", "wget", "mcrypt", "nscd", "htop", "zip", "unzip", "mc", "libzip5"]

initd_script = """#!/bin/sh
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

def getVersion():
    try: return subprocess.check_output("lsb_release -d".split()).split(":")[-1].strip()
    except: return ""

def prepare():
    global rPackages
    for rFile in ["/var/lib/dpkg/lock-frontend", "/var/cache/apt/archives/lock", "/var/lib/dpkg/lock"]:
        try: os.remove(rFile)
        except: pass
    os.system("apt-get update > /dev/null")
#    os.system("apt-get remove --auto-remove libcurl4 -y > /dev/null")
    for rPackage in rPackages: os.system("apt-get install %s -y > /dev/null" % rPackage)
    os.system("apt-get install -y > /dev/null") # Clean up above
    os.system("adduser --system --shell /bin/false --group --disabled-login xtreamcodes > /dev/null")
    if not os.path.exists("/home/xtreamcodes"): os.mkdir("/home/xtreamcodes")
    return True

def install():
    global rDownloadURL
    rURL = rDownloadURL
    os.system('wget -q -O "/tmp/xtreamcodes.zip" "%s"' % rURL)
    if os.path.exists("/tmp/xtreamcodes.zip"):
        os.system('unzip "/tmp/xtreamcodes.zip" -d "/home/xtreamcodes/" > /dev/null')
        try: os.remove("/tmp/xtreamcodes.zip")
        except: pass
        return True
    return False

def encrypt(rHost="127.0.0.1", rUsername="user_iptvpro", rPassword="", rDatabase="xtream_iptvpro", rServerID=1, rPort=7999):
    try: os.remove("/home/xtreamcodes/iptv_xtream_codes/config")
    except: pass
    rf = open('/home/xtreamcodes/iptv_xtream_codes/config', 'wb')
    lestring=''.join(chr(ord(c)^ord(k)) for c,k in zip('{\"host\":\"%s\",\"db_user\":\"%s\",\"db_pass\":\"%s\",\"db_name\":\"%s\",\"server_id\":\"%d\", \"db_port\":\"%d\"}' % (rHost, rUsername, rPassword, rDatabase, rServerID, rPort), cycle('5709650b0d7806074842c6de575025b1')))
    rf.write(base64.b64encode(bytes(lestring, 'ascii')))
    rf.close()

def configure():
    global initd_script
    if not "/home/xtreamcodes/iptv_xtream_codes/" in open("/etc/fstab").read():
        rFile = open("/etc/fstab", "a")
        rFile.write("tmpfs /home/xtreamcodes/iptv_xtream_codes/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\ntmpfs /home/xtreamcodes/iptv_xtream_codes/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=2G 0 0")
        rFile.close()
    if not "xtreamcodes" in open("/etc/sudoers").read(): os.system('echo "xtreamcodes ALL = (root) NOPASSWD: /sbin/iptables" >> /etc/sudoers')
    if not os.path.exists("/etc/init.d/xtreamcodes"):
        rFile = open("/etc/init.d/xtreamcodes", "w")
        rFile.write(initd_script)
        rFile.close()
        os.system("chmod +x /etc/init.d/xtreamcodes > /dev/null")
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/xtreamcodes"): 
        os.system("wget -q https://github.com/xoceunder/Xtream-UI-install/raw/main/xtreamcodes -O /home/xtreamcodes/iptv_xtream_codes/xtreamcodes")
        os.system("sudo chmod +x /home/xtreamcodes/iptv_xtream_codes/xtreamcodes")
    try: os.remove("/usr/bin/ffmpeg")
    except: pass
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/tv_archive"): os.mkdir("/home/xtreamcodes/iptv_xtream_codes/tv_archive/")
    os.system("ln -s /home/xtreamcodes/iptv_xtream_codes/bin/ffmpeg /usr/bin/")
    os.system("chattr -i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null")
    os.system("wget -q https://bitbucket.org/xoceunder/xtream-ui-install/raw/main/GeoLite2.mmdb -O /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb")
    os.system("wget -q https://bitbucket.org/xoceunder/xtream-ui-install/raw/main/pid_monitor.php -O /home/xtreamcodes/iptv_xtream_codes/crons/pid_monitor.php")
    os.system("chown xtreamcodes:xtreamcodes -R /home/xtreamcodes > /dev/null")
    os.system("chmod -R 0777 /home/xtreamcodes > /dev/null")
    os.system("chattr +i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null")
    os.system("sed -i 's|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes 2>/dev/null|g' /home/xtreamcodes/iptv_xtream_codes/start_services.sh")
    os.system("chmod +x /home/xtreamcodes/iptv_xtream_codes/start_services.sh > /dev/null")
    os.system("mount -a")
    os.system("chmod 0700 /home/xtreamcodes/iptv_xtream_codes/config > /dev/null")
    os.system("sed -i 's|echo \"Xtream Codes Reborn\";|header(\"Location: https://www.google.com/\");|g' /home/xtreamcodes/iptv_xtream_codes/wwwdir/index.php")
    if not "api.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    api.xtream-codes.com" >> /etc/hosts')
    if not "downloads.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    downloads.xtream-codes.com" >> /etc/hosts')
    if not "xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    xtream-codes.com" >> /etc/hosts')
    if not "@reboot root /home/xtreamcodes/iptv_xtream_codes/start_services.sh" in open("/etc/crontab").read(): os.system('echo "@reboot root /home/xtreamcodes/iptv_xtream_codes/start_services.sh" >> /etc/crontab')

def start(): os.system("sudo /etc/init.d/xtreamcodes start > /dev/null")

def setPorts(rPorts):
    os.system("sed -i 's/listen 25461;/listen %d;/g' /home/xtreamcodes/iptv_xtream_codes/nginx/conf/nginx.conf" % rPorts[0])
    os.system("sed -i 's/:25461/:%d/g' /home/xtreamcodes/iptv_xtream_codes/nginx_rtmp/conf/nginx.conf" % rPorts[0])
    os.system("sed -i 's/listen 25463 ssl;/listen %d ssl;/g' /home/xtreamcodes/iptv_xtream_codes/nginx/conf/nginx.conf" % rPorts[1])
    os.system("sed -i 's/listen 25462;/listen %d;/g' /home/xtreamcodes/iptv_xtream_codes/nginx_rtmp/conf/nginx.conf" % rPorts[2])

if __name__ == "__main__":
    rHost = sys.argv[1]
    rPort = int(sys.argv[2])
    rUsername = sys.argv[3]
    rPassword = sys.argv[4]
    rDatabase = sys.argv[5]
    rServerID = int(sys.argv[6])
    try: rPorts = [int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])]
    except: rPorts = None
    rRet = prepare()
    if not install(): sys.exit(1)
    encrypt(rHost, rUsername, rPassword, rDatabase, rServerID, rPort)
    configure()
    if rPorts: setPorts(rPorts)
    start()
    

