#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess, os, sys, socket
from itertools import cycle, izip

rDownloadURL = "https://bitbucket.org/xoceunder/xtream-ui-install/raw/main/sub_xui_xoceunder.zip"
rPackages = ["python", "libcurl4", "libxslt1-dev", "libgeoip-dev", "libonig-dev", "e2fsprogs", "wget", "mcrypt", "nscd", "htop", "zip", "unzip", "mc"]
rRemove = ["mysql-server"]
rSysCtl = "# XtreamCodes\n\nnet.ipv4.tcp_congestion_control = bbr\nnet.core.default_qdisc = fq\nnet.ipv4.tcp_rmem = 8192 87380 134217728\nnet.ipv4.udp_rmem_min = 16384\nnet.core.rmem_default = 262144\nnet.core.rmem_max = 268435456\nnet.ipv4.tcp_wmem = 8192 65536 134217728\nnet.ipv4.udp_wmem_min = 16384\nnet.core.wmem_default = 262144\nnet.core.wmem_max = 268435456\nnet.core.somaxconn = 1000000\nnet.core.netdev_max_backlog = 250000\nnet.core.optmem_max = 65535\nnet.ipv4.tcp_max_tw_buckets = 1440000\nnet.ipv4.tcp_max_orphans = 16384\nnet.ipv4.ip_local_port_range = 2000 65000\nnet.ipv4.tcp_no_metrics_save = 1\nnet.ipv4.tcp_slow_start_after_idle = 0\nnet.ipv4.tcp_fin_timeout = 15\nnet.ipv4.tcp_keepalive_time = 300\nnet.ipv4.tcp_keepalive_probes = 5\nnet.ipv4.tcp_keepalive_intvl = 15\nfs.file-max=20970800\nfs.nr_open=20970800\nfs.aio-max-nr=20970800\nnet.ipv4.tcp_timestamps = 1\nnet.ipv4.tcp_window_scaling = 1\nnet.ipv4.tcp_mtu_probing = 1\nnet.ipv4.route.flush = 1\nnet.ipv6.route.flush = 1"

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
    
def is_installed(package_name):
    try:
        subprocess.run(['dpkg', '-s', package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def prepare():
    global rPackages, rRemove
    for rFile in ["/var/lib/dpkg/lock-frontend","/var/cache/apt/archives/lock","/var/lib/dpkg/lock"]:
        if os.path.exists(rFile):
            try:
                os.remove(rFile)
            except:
                pass
    os.system("apt-get update > /dev/null 2>&1")
    os.system("apt-get -y full-upgrade > /dev/null 2>&1")
    for rPackage in rRemove:
        if is_installed(rPackage):
            os.system("sudo DEBIAN_FRONTEND=noninteractive apt-get remove %s > /dev/null" % rPackage)
    for rPackage in rPackages:
        if not is_installed(rPackage):
            subprocess.run(f"sudo DEBIAN_FRONTEND=noninteractive apt-get install {rPackage} -yq > /dev/null 2>&1", shell=True)
    os.system("apt-get install -y > /dev/null") # Clean up above
    os.system("adduser --system --shell /bin/false --group --disabled-login xtreamcodes > /dev/null")
    if not os.path.exists("/home/xtreamcodes"): os.mkdir("/home/xtreamcodes")
    return True
 
def install():
    global rInstall, rDownloadURL
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
    rf.write(''.join(chr(ord(c)^ord(k)) for c,k in izip('{\"host\":\"%s\",\"db_user\":\"%s\",\"db_pass\":\"%s\",\"db_name\":\"%s\",\"server_id\":\"%d\", \"db_port\":\"%d\"}' % (rHost, rUsername, rPassword, rDatabase, rServerID, rPort), cycle('5709650b0d7806074842c6de575025b1'))).encode('base64').replace('\n', ''))
    rf.close()

def configure():
    if not "/home/xtreamcodes/iptv_xtream_codes/" in open("/etc/fstab").read():
        rFile = open("/etc/fstab", "a")
        rFile.write("tmpfs /home/xtreamcodes/iptv_xtream_codes/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\ntmpfs /home/xtreamcodes/iptv_xtream_codes/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=2G 0 0")
        rFile.close()
    if not "xtreamcodes" in open("/etc/sudoers").read(): os.system('echo "xtreamcodes ALL = (root) NOPASSWD: /sbin/iptables, /usr/bin/chattr, /usr/bin/python3, /usr/bin/python" >> /etc/sudoers')
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/xtreamcodes"): 
        os.system("wget -q https://github.com/xoceunder/Xtream-UI-install/raw/main/xtreamcodes -O /home/xtreamcodes/iptv_xtream_codes/xtreamcodes")
        os.system("sudo chmod +x /home/xtreamcodes/iptv_xtream_codes/xtreamcodes")
    if not os.path.exists("/etc/init.d/xtreamcodes"):
        with io.open("/etc/init.d/xtreamcodes", "w", encoding="utf-8") as f:
            f.write(initd_script)
        os.system("sudo chmod +x /etc/init.d/xtreamcodes")
        os.system("sudo update-rc.d xtreamcodes defaults")
    os.system("sudo modprobe ip_conntrack")
    rFile = open("/etc/sysctl.conf", "w", encoding="utf-8")
    rFile.write(rSysCtl)
    rFile.close()
    os.system("sudo sysctl -p >/dev/null 2>&1")
    rFile = open("/home/xtreamcodes/iptv_xtream_codes/sysctl.on", "w")
    rFile.close()
    if not "DefaultLimitNOFILE=655350" in open("/etc/systemd/system.conf").read():
        os.system('sudo echo "\nDefaultLimitNOFILE=655350" >> "/etc/systemd/system.conf"')
        os.system('sudo echo "\nDefaultLimitNOFILE=655350" >> "/etc/systemd/user.conf"')
    try: os.remove("/usr/bin/ffmpeg")
    except: pass
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/tv_archive"): os.mkdir("/home/xtreamcodes/iptv_xtream_codes/tv_archive/")
    os.system("ln -s /home/xtreamcodes/iptv_xtream_codes/bin/ffmpeg /usr/bin/")
    os.system("wget -q https://bitbucket.org/xoceunder/xtream-ui-install/raw/main/GeoLite2.mmdb -O /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb")
    os.system("chattr -ai /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null")
    os.system("sudo chmod 0777 /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null")
    os.system("wget -q https://bitbucket.org/xoceunder/xtream-ui-install/raw/main/pid_monitor.php -O /home/xtreamcodes/iptv_xtream_codes/crons/pid_monitor.php")
    os.system("chown xtreamcodes:xtreamcodes -R /home/xtreamcodes > /dev/null")
    os.system("chmod -R 0777 /home/xtreamcodes > /dev/null")
    os.system("sed -i 's|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes 2>/dev/null|g' /home/xtreamcodes/iptv_xtream_codes/start_services.sh")
    os.system("chmod +x /home/xtreamcodes/iptv_xtream_codes/start_services.sh > /dev/null")
    os.system("mount -a")
    os.system("chown xtreamcodes:xtreamcodes /home/xtreamcodes/iptv_xtream_codes/config")
    os.system("chmod 0700 /home/xtreamcodes/iptv_xtream_codes/config > /dev/null")
    os.system("sed -i 's|echo \"Xtream Codes Reborn\";|header(\"Location: https://www.google.com/\");|g' /home/xtreamcodes/iptv_xtream_codes/wwwdir/index.php")
    if not "api.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    api.xtream-codes.com" >> /etc/hosts')
    if not "downloads.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    downloads.xtream-codes.com" >> /etc/hosts')
    if not "xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    xtream-codes.com" >> /etc/hosts')
    if not "@reboot root /etc/init.d/xtreamcodes start" in open("/etc/crontab").read(): os.system('echo "@reboot root /etc/init.d/xtreamcodes start" >> /etc/crontab')

def start(): os.system("sudo /etc/init.d/xtreamcodes start > /dev/null")

def setPorts(rPorts):
    os.system("sed -i 's/listen 25461;/listen %d;/g' /home/xtreamcodes/iptv_xtream_codes/nginx/conf/nginx.conf" % rPorts[0])
    os.system("sed -i 's/:25461/:%d/g' /home/xtreamcodes/iptv_xtream_codes/nginx_rtmp/conf/nginx.conf" % rPorts[0])
    os.system("sed -i 's/listen 25463 ssl;/listen %d ssl;/g' /home/xtreamcodes/iptv_xtream_codes/nginx/conf/nginx.conf" % rPorts[1])
    os.system("sed -i 's/listen 25462;/listen %d;/g' /home/xtreamcodes/iptv_xtream_codes/nginx_rtmp/conf/nginx.conf" % rPorts[2])
   
if __name__ == "__main__":
    try: rVersion = os.popen('lsb_release -sr').read().strip()
    except: rVersion = None
    if rVersion == "20.04":
        rPackages.append("libzip5")
    elif rVersion == "18.04":
        rPackages.append("libzip4")
    else:
        rPackages.append("libzip5")
    rHost = sys.argv[1]
    rPort = int(sys.argv[2])
    rUsername = sys.argv[3]
    rPassword = sys.argv[4]
    rDatabase = sys.argv[5]
    rServerID = int(sys.argv[6])
    try: rPorts = [int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])]
    except: rPorts = None
    prepare()
    if not install(): sys.exit(1)
    encrypt(rHost, rUsername, rPassword, rDatabase, rServerID, rPort)
    configure()
    if rPorts: setPorts(rPorts)
    start()
