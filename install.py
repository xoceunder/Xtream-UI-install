#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess, os, random, string, sys, shutil, socket, zipfile, json, base64, io, time
from itertools import cycle
from zipfile import ZipFile
from urllib.request import urlopen

rDownloadURL = {"main": "https://bitbucket.org/xoceunder/xtream-ui-install/raw/main/main_xui_xoceunder.zip", "sub": "https://bitbucket.org/xoceunder/xtream-ui-install/raw/main/sub_xui_xoceunder.zip"}
rPackages = ["cpufrequtils", "iproute2", "python", "net-tools", "dirmngr", "gpg-agent", "software-properties-common", "libcurl4", "libxslt1-dev", "libgeoip-dev", "libonig-dev", "e2fsprogs", "wget", "sysstat", "alsa-utils", "v4l-utils", "mcrypt", "nscd", "htop", "iptables-persistent", "libjpeg-dev", "libpng-dev", "php-ssh2", "xz-utils", "zip", "unzip", "mc", "libpng16-16", "libzip5", "mariadb-server", "rsync", "libmaxminddb0", "libmaxminddb-dev", "python3-paramiko", "python-is-python3"]
rRemove = ["mysql-server"]
rInstall = {"MAIN": "main", "LB": "sub"}
rUpdate = {"UPDATE": "update"}
rMySQLCnf = base64.b64decode("IyBYdHJlYW0gQ29kZXMKCltjbGllbnRdCnBvcnQgICAgICAgICAgICA9IDMzMDYKCltteXNxbGRfc2FmZV0KbmljZSAgICAgICAgICAgID0gMAoKW215c3FsZF0KdXNlciAgICAgICAgICAgID0gbXlzcWwKcG9ydCAgICAgICAgICAgID0gNzk5OQpiYXNlZGlyICAgICAgICAgPSAvdXNyCmRhdGFkaXIgICAgICAgICA9IC92YXIvbGliL215c3FsCnRtcGRpciAgICAgICAgICA9IC90bXAKbGMtbWVzc2FnZXMtZGlyID0gL3Vzci9zaGFyZS9teXNxbApza2lwLWV4dGVybmFsLWxvY2tpbmcKc2tpcC1uYW1lLXJlc29sdmU9MQoKYmluZC1hZGRyZXNzICAgICAgICAgICAgPSAqCmtleV9idWZmZXJfc2l6ZSA9IDEyOE0KCm15aXNhbV9zb3J0X2J1ZmZlcl9zaXplID0gNE0KbWF4X2FsbG93ZWRfcGFja2V0ICAgICAgPSA2NE0KbXlpc2FtLXJlY292ZXItb3B0aW9ucyA9IEJBQ0tVUAptYXhfbGVuZ3RoX2Zvcl9zb3J0X2RhdGEgPSA4MTkyCnF1ZXJ5X2NhY2hlX2xpbWl0ICAgICAgID0gNE0KcXVlcnlfY2FjaGVfc2l6ZSAgICAgICAgPSAwCnF1ZXJ5X2NhY2hlX3R5cGUJPSAwCgpleHBpcmVfbG9nc19kYXlzICAgICAgICA9IDEwCm1heF9iaW5sb2dfc2l6ZSAgICAgICAgID0gMTAwTQoKbWF4X2Nvbm5lY3Rpb25zICA9IDIwMDAgI3JlY29tbWVuZGVkIGZvciAxNkdCIHJhbSAKYmFja19sb2cgPSA0MDk2Cm9wZW5fZmlsZXNfbGltaXQgPSAxNjM4NAppbm5vZGJfb3Blbl9maWxlcyA9IDE2Mzg0Cm1heF9jb25uZWN0X2Vycm9ycyA9IDMwNzIKdGFibGVfb3Blbl9jYWNoZSA9IDQwOTYKdGFibGVfZGVmaW5pdGlvbl9jYWNoZSA9IDQwOTYKCgp0bXBfdGFibGVfc2l6ZSA9IDFHCm1heF9oZWFwX3RhYmxlX3NpemUgPSAxRwoKaW5ub2RiX2J1ZmZlcl9wb29sX3NpemUgPSAxMkcgI3JlY29tbWVuZGVkIGZvciAxNkdCIHJhbQppbm5vZGJfYnVmZmVyX3Bvb2xfaW5zdGFuY2VzID0gMQppbm5vZGJfcmVhZF9pb190aHJlYWRzID0gNjQKaW5ub2RiX3dyaXRlX2lvX3RocmVhZHMgPSA2NAppbm5vZGJfdGhyZWFkX2NvbmN1cnJlbmN5ID0gMAppbm5vZGJfZmx1c2hfbG9nX2F0X3RyeF9jb21taXQgPSAwCmlubm9kYl9mbHVzaF9tZXRob2QgPSBPX0RJUkVDVApwZXJmb3JtYW5jZV9zY2hlbWEgPSBPTgppbm5vZGItZmlsZS1wZXItdGFibGUgPSAxCmlubm9kYl9pb19jYXBhY2l0eT0yMDAwMAppbm5vZGJfdGFibGVfbG9ja3MgPSAwCmlubm9kYl9sb2NrX3dhaXRfdGltZW91dCA9IDAKaW5ub2RiX2RlYWRsb2NrX2RldGVjdCA9IDAKaW5ub2RiX2xvZ19maWxlX3NpemUgPSA1MTJNCgpzcWwtbW9kZT0iTk9fRU5HSU5FX1NVQlNUSVRVVElPTiIKCltteXNxbGR1bXBdCnF1aWNrCnF1b3RlLW5hbWVzCm1heF9hbGxvd2VkX3BhY2tldCAgICAgID0gMTZNCgpbbXlzcWxdCgpbaXNhbWNoa10Ka2V5X2J1ZmZlcl9zaXplICAgICAgICAgICAgICA9IDE2TQo=")
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

if sys.version_info.major != 3:
    printc("Please run with python3.")
    sys.exit(1)

rPath = os.path.dirname(os.path.realpath(__file__))

rVersions = {
    "18.04": "bionic",
    "20.04": "focal",
    "22.04": "jammy",
    "24.04": "noble"
}

class col:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m' # orange on some systems
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

def generate(length=19): return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def getVersion():
    try: return os.popen("lsb_release -d").read().strip()
    except: return ""
    
def getCodename():
    try: return os.popen("lsb_release -sc").read().strip()
    except: return ""

def printc(rText, rColour=col.BRIGHT_GREEN, rPadding=0, rLimit=46):
    print("%s ┌─────────────────────────────────────────────────┐ %s" % (rColour, col.ENDC))
    for i in range(rPadding): print("%s │                                                 │ %s" % (rColour, col.ENDC))
    array = [rText[i:i+rLimit] for i in range(0, len(rText), rLimit)]
    for i in array : print("%s │ %s%s%s │ %s" % (rColour, " "*round(23-(len(i)/2)), i, " "*round(46-(22-(len(i)/2))-len(i)), col.ENDC))
    for i in range(rPadding): print("%s │                                                 │ %s" % (rColour, col.ENDC))
    print("%s └─────────────────────────────────────────────────┘ %s" % (rColour, col.ENDC))
    print(" ")
    
def is_installed(package_name):
    try:
        subprocess.run(['dpkg', '-s', package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def prepare(rType="MAIN"):
    global rPackages, rRemove, rVersions
    if rType != "MAIN": rPackages = rPackages[:-1]
    printc("Preparing Installation")
    if os.path.isfile('/home/xtreamcodes/iptv_xtream_codes/config'):
        shutil.copyfile('/home/xtreamcodes/iptv_xtream_codes/config', '/tmp/config.xtmp')
    for rFile in ["/var/lib/dpkg/lock-frontend","/var/cache/apt/archives/lock","/var/lib/dpkg/lock"]:
        if os.path.exists(rFile):
            try:
                os.remove(rFile)
            except:
                pass
    printc("Updating Operating System")
    os.system("apt-get update > /dev/null 2>&1")
    os.system("apt-get -y full-upgrade > /dev/null 2>&1")
    if rType == "MAIN":
        os.system("sudo apt-get -yq install software-properties-common > /dev/null 2>&1")
        printc("Adding repo: Ubuntu %s" % getCodename())
        os.system("sudo apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc' > /dev/null 2>&1")
        os.system("sudo add-apt-repository -y 'deb [arch=amd64,arm64,ppc64el] http://mirror.23media.com/mariadb/repo/11.5/ubuntu %s main' > /dev/null 2>&1" % getCodename())
        os.system("apt-get update > /dev/null 2>&1")
    for rPackage in rRemove:
        if is_installed(rPackage):
            printc("Removing %s" % rPackage)
            os.system("sudo DEBIAN_FRONTEND=noninteractive apt-get remove %s > /dev/null" % rPackage)
    for rPackage in rPackages:
        if not is_installed(rPackage):
            printc("Installing %s" % rPackage)
            subprocess.run(f"sudo DEBIAN_FRONTEND=noninteractive apt-get install {rPackage} -yq > /dev/null 2>&1", shell=True)
    os.system("apt-get install -f -y > /dev/null") # Clean up above
    os.system("systemctl start mariadb > /dev/null")
    try:
        subprocess.check_output("getent passwd xtreamcodes > /dev/null".split())
    except:
        # Create User
        printc("Creating user xtreamcodes")
        os.system("adduser --system --shell /bin/false --group --disabled-login xtreamcodes > /dev/null")
    if not os.path.exists("/home/xtreamcodes"): os.mkdir("/home/xtreamcodes")
    return True

def install(rType="MAIN"):
    global rInstall, rDownloadURL
    printc("Downloading Software")
    try: rURL = rDownloadURL[rInstall[rType]]
    except:
        printc("Invalid download URL!", col.BRIGHT_RED)
        return False
    os.system('wget -q -O "/tmp/xtreamcodes.zip" "%s"' % rURL)
    if os.path.exists("/tmp/xtreamcodes.zip"):
        printc("Installing Software")
        os.system('unzip "/tmp/xtreamcodes.zip" -d "/home/xtreamcodes/" > /dev/null')
        if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/xtreamcodes"): 
            os.system("wget -q https://github.com/xoceunder/Xtream-UI-install/raw/main/xtreamcodes -O /home/xtreamcodes/iptv_xtream_codes/xtreamcodes")
            os.system("sudo chmod +x /home/xtreamcodes/iptv_xtream_codes/xtreamcodes")
        try: os.remove("/tmp/xtreamcodes.zip")
        except: pass
        return True
    printc("Failed to download installation file!", col.BRIGHT_RED)
    return False
    
def update(rType="MAIN"):
    if rType == "UPDATE":
        printc("Enter the link of release_xyz.zip file:", col.BRIGHT_RED)
        rlink = input('Example: https://bitbucket.org/xoceunder/xtream-ui-install/raw/main/release_22f.zip\n\nNow enter the link:\n\n')
    else:
        rlink = "https://bitbucket.org/xoceunder/xtream-ui-install/raw/main/release_22f.zip"
        printc("Downloading Software Update")  
    os.system('wget -q -O "/tmp/update.zip" "%s"' % rlink)
    if os.path.exists("/tmp/update.zip"):
        try: is_ok = zipfile.ZipFile("/tmp/update.zip")
        except:
            printc("Invalid link or zip file is corrupted!", col.BRIGHT_RED)
            os.remove("/tmp/update.zip")
            return False
    rURL = rlink
    printc("Installing Admin Panel")
    if os.path.exists("/tmp/update.zip"):
        try: is_ok = zipfile.ZipFile("/tmp/update.zip")
        except:
            printc("Invalid link or zip file is corrupted!", col.BRIGHT_RED)
            os.remove("/tmp/update.zip")
            return False
        printc("Updating Software")
        os.system('chattr -i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null && rm -rf /home/xtreamcodes/iptv_xtream_codes/admin > /dev/null && rm -rf /home/xtreamcodes/iptv_xtream_codes/pytools > /dev/null && unzip /tmp/update.zip -d /tmp/update/ > /dev/null && cp -rf /tmp/update/XtreamUI-master/* /home/xtreamcodes/iptv_xtream_codes/ > /dev/null && rm -rf /tmp/update/XtreamUI-master > /dev/null && rm -rf /tmp/update > /dev/null && chown -R xtreamcodes:xtreamcodes /home/xtreamcodes/ > /dev/null && chmod +x /home/xtreamcodes/iptv_xtream_codes/permissions.sh > /dev/null && chattr +i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null')
        if not "sudo chmod 400 /home/xtreamcodes/iptv_xtream_codes/config" in open("/home/xtreamcodes/iptv_xtream_codes/permissions.sh").read(): os.system('echo "#!/bin/bash\nsudo chmod -R 777 /home/xtreamcodes 2>/dev/null\nsudo find /home/xtreamcodes/iptv_xtream_codes/admin/ -type f -exec chmod 644 {} \; 2>/dev/null\nsudo find /home/xtreamcodes/iptv_xtream_codes/admin/ -type d -exec chmod 755 {} \; 2>/dev/null\nsudo find /home/xtreamcodes/iptv_xtream_codes/wwwdir/ -type f -exec chmod 644 {} \; 2>/dev/null\nsudo find /home/xtreamcodes/iptv_xtream_codes/wwwdir/ -type d -exec chmod 755 {} \; 2>/dev/null\nsudo chmod +x /home/xtreamcodes/iptv_xtream_codes/nginx/sbin/nginx 2>/dev/null\nsudo chmod +x /home/xtreamcodes/iptv_xtream_codes/nginx_rtmp/sbin/nginx_rtmp 2>/dev/null\nsudo chmod 400 /home/xtreamcodes/iptv_xtream_codes/config 2>/dev/null" > /home/xtreamcodes/iptv_xtream_codes/permissions.sh')
        os.system("/home/xtreamcodes/iptv_xtream_codes/permissions.sh > /dev/null")
        try: os.remove("/tmp/update.zip")
        except: pass
        return True
    printc("Failed to download installation file!", col.BRIGHT_RED)
    return False

def mysql(rUsername, rPassword):
    global rMySQLCnf
    printc("Configuring MySQL")
    rCreate = True
    if os.path.exists("/etc/mysql/my.cnf"):
        if open("/etc/mysql/my.cnf", "r").read(14) == "# Xtream Codes": rCreate = False
    if rCreate:
        shutil.copy("/etc/mysql/my.cnf", "/etc/mysql/my.cnf.xc")
        rFile = open("/etc/mysql/my.cnf", "wb")
        rFile.write(rMySQLCnf)
        rFile.close()
        os.system("systemctl restart mariadb > /dev/null")
    #printc("Enter MySQL Root Password:", col.BRIGHT_RED)
    for i in range(5):
        rMySQLRoot = "" #raw_input("  ")
        print(" ")
        if len(rMySQLRoot) > 0: rExtra = " -p%s" % rMySQLRoot
        else: rExtra = ""
        rDrop = True
        try:
            if rDrop:
                os.system('mariadb -u root%s -e "DROP DATABASE IF EXISTS xtream_iptvpro; CREATE DATABASE IF NOT EXISTS xtream_iptvpro;" > /dev/null' % rExtra)
                os.system('mariadb -u root%s -e "USE xtream_iptvpro; DROP USER IF EXISTS \'%s\'@\'%%\';" > /dev/null' % (rExtra, rUsername))
                os.system("mariadb -u root%s xtream_iptvpro < /home/xtreamcodes/iptv_xtream_codes/database.sql > /dev/null" % rExtra)
                os.system('mariadb -u root%s -e "USE xtream_iptvpro; UPDATE settings SET live_streaming_pass = \'%s\', unique_id = \'%s\', crypt_load_balancing = \'%s\';" > /dev/null' % (rExtra, generate(20), generate(10), generate(20)))
                os.system('mariadb -u root%s -e "USE xtream_iptvpro; REPLACE INTO streaming_servers (id, server_name, domain_name, server_ip, vpn_ip, ssh_password, ssh_port, diff_time_main, http_broadcast_port, total_clients, system_os, network_interface, latency, status, enable_geoip, geoip_countries, last_check_ago, can_delete, server_hardware, total_services, persistent_connections, rtmp_port, geoip_type, isp_names, isp_type, enable_isp, boost_fpm, http_ports_add, network_guaranteed_speed, https_broadcast_port, https_ports_add, whitelist_ips, watchdog_data, timeshift_only) VALUES (1, \'Main Server\', \'\', \'%s\', \'\', NULL, NULL, 0, 25461, 1000, \'%s\', \'eth0\', 0, 1, 0, \'\', 0, 0, \'{}\', 3, 0, 25462, \'low_priority\', \'\', \'low_priority\', 0, 1, \'\', 1000, 25463, \'\', \'[\"127.0.0.1\",\"\"]\', \'{}\', 0);" > /dev/null' % (rExtra, getIP(), getVersion()))
                os.system('mariadb -u root%s -e "USE xtream_iptvpro; REPLACE INTO reg_users (id, username, password, email, member_group_id, verified, status) VALUES (1, \'admin\', \'\$6\$rounds=20000\$xtreamcodes\$XThC5OwfuS0YwS4ahiifzF14vkGbGsFF1w7ETL4sRRC5sOrAWCjWvQJDromZUQoQuwbAXAFdX3h3Cp3vqulpS0\', \'admin@website.com\', 1, 1, 1);" > /dev/null'  % rExtra)
                os.system('mariadb -u root%s -e "CREATE USER \'%s\'@\'%%\' IDENTIFIED BY \'%s\'; GRANT ALL PRIVILEGES ON xtream_iptvpro.* TO \'%s\'@\'%%\' WITH GRANT OPTION; GRANT SELECT, LOCK TABLES ON *.* TO \'%s\'@\'%%\';FLUSH PRIVILEGES;" > /dev/null' % (rExtra, rUsername, rPassword, rUsername, rUsername))
                os.system('mariadb -u root%s -e "USE xtream_iptvpro; CREATE TABLE IF NOT EXISTS dashboard_statistics (id int(11) NOT NULL AUTO_INCREMENT, type varchar(16) NOT NULL DEFAULT \'\', time int(16) NOT NULL DEFAULT \'0\', count int(16) NOT NULL DEFAULT \'0\', PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=latin1; INSERT INTO dashboard_statistics (type, time, count) VALUES(\'conns\', UNIX_TIMESTAMP(), 0),(\'users\', UNIX_TIMESTAMP(), 0);\" > /dev/null' % rExtra)
            try: os.remove("/home/xtreamcodes/iptv_xtream_codes/database.sql")
            except: pass
            return True
        except: printc("Invalid password! Try again", col.BRIGHT_RED)
    return False

def encrypt(rHost="127.0.0.1", rUsername="user_iptvpro", rPassword="", rDatabase="xtream_iptvpro", rServerID=1, rPort=7999):
    if os.path.isfile('/home/xtreamcodes/iptv_xtream_codes/config'):
        rDecrypt = decrypt()
        rHost = rDecrypt["host"]
        rPassword = rDecrypt["db_pass"]
        rServerID = int(rDecrypt["server_id"])
        rUsername = rDecrypt["db_user"]
        rDatabase = rDecrypt["db_name"]
        rPort = int(rDecrypt["db_port"])
    printc("Encrypting...")
    try: os.remove("/home/xtreamcodes/iptv_xtream_codes/config")
    except: pass

    rf = open('/home/xtreamcodes/iptv_xtream_codes/config', 'wb')
    lestring=''.join(chr(ord(c)^ord(k)) for c,k in zip('{\"host\":\"%s\",\"db_user\":\"%s\",\"db_pass\":\"%s\",\"db_name\":\"%s\",\"server_id\":\"%d\", \"db_port\":\"%d\"}' % (rHost, rUsername, rPassword, rDatabase, rServerID, rPort), cycle('5709650b0d7806074842c6de575025b1')))
    rf.write(base64.b64encode(bytes(lestring, 'ascii')))
    rf.close()


def decrypt():
    rConfigPath = "/home/xtreamcodes/iptv_xtream_codes/config"
    try: return json.loads(''.join(chr(c^ord(k)) for c,k in zip(base64.b64decode(open(rConfigPath, 'rb').read()), cycle('5709650b0d7806074842c6de575025b1'))))
    except: return None

def configure():
    printc("Configuring System")
    if not "/home/xtreamcodes/iptv_xtream_codes/" in open("/etc/fstab").read():
        rFile = open("/etc/fstab", "a", encoding="utf-8")
        rFile.write("tmpfs /home/xtreamcodes/iptv_xtream_codes/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\ntmpfs /home/xtreamcodes/iptv_xtream_codes/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=2G 0 0")
        rFile.close()
    if not "xtreamcodes" in open("/etc/sudoers").read():
        os.system('echo "xtreamcodes ALL = (root) NOPASSWD: /sbin/iptables, /usr/bin/chattr, /usr/bin/python3, /usr/bin/python" >> /etc/sudoers')
    if os.path.exists("/etc/init.d/xtreamcodes"):
        os.remove("/etc/init.d/xtreamcodes")
    if not os.path.exists("/etc/init.d/xtreamcodes"):
        with io.open("/etc/init.d/xtreamcodes", "w", encoding="utf-8") as f:
            f.write(initd_script)
        os.system("sudo chmod +x /etc/init.d/xtreamcodes")
        os.system("sudo update-rc.d xtreamcodes defaults")
    printc("Service XtreamCodes installed in /etc/init.d/xtreamcodes")
    printc("Custom sysctl.conf - If you have your own custom sysctl.conf, type N or it will be overwritten. If you don't know what a sysctl configuration is, type Y as it will correctly set your TCP settings and open file limits.", col.BRIGHT_YELLOW)
    print(" ")
    while True:
        rAnswer = input("Overwrite sysctl configuration? Recommended! (Y / N): ")
        if rAnswer.upper() in ["Y", "N"]:
            break
    if rAnswer.upper() == "Y":
        try:
            os.system("sudo modprobe ip_conntrack")
        except:
            pass
        try:
            rFile = open("/etc/sysctl.conf", "w", encoding="utf-8")
            rFile.write(rSysCtl)
            rFile.close()
            os.system("sudo sysctl -p >/dev/null 2>&1")
            rFile = open("/home/xtreamcodes/iptv_xtream_codes/sysctl.on", "w")
            rFile.close()
        except:
            printc("Failed to write to sysctl file.", col.BRIGHT_RED)
    else:
        if os.path.exists("/home/xtreamcodes/iptv_xtream_codes/sysctl.on"):
            os.remove("/home/xtreamcodes/iptv_xtream_codes/sysctl.on")
    if not "DefaultLimitNOFILE=655350" in open("/etc/systemd/system.conf").read():
        os.system('sudo echo "\nDefaultLimitNOFILE=655350" >> "/etc/systemd/system.conf"')
        os.system('sudo echo "\nDefaultLimitNOFILE=655350" >> "/etc/systemd/user.conf"')
    try: os.remove("/usr/bin/ffmpeg")
    except: pass
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/tv_archive"): os.mkdir("/home/xtreamcodes/iptv_xtream_codes/tv_archive/")
    os.system("ln -s /home/xtreamcodes/iptv_xtream_codes/bin/ffmpeg /usr/bin/")
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb"): os.system("wget -q https://bitbucket.org/xoceunder/xtream-ui-install/raw/main/GeoLite2.mmdb -O /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb")
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/crons/pid_monitor.php"): os.system("wget -q https://bitbucket.org/xoceunder/xtream-ui-install/raw/main/pid_monitor.php -O /home/xtreamcodes/iptv_xtream_codes/crons/pid_monitor.php")
    os.system("chown xtreamcodes:xtreamcodes -R /home/xtreamcodes > /dev/null")
    os.system("chmod -R 0777 /home/xtreamcodes > /dev/null")
    os.system("chattr -ai /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null")
    os.system("sudo chmod 0777 /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null")
    os.system("sed -i 's|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes 2>/dev/null|g' /home/xtreamcodes/iptv_xtream_codes/start_services.sh")
    os.system("chmod +x /home/xtreamcodes/iptv_xtream_codes/start_services.sh > /dev/null")
    os.system("sudo mount -a  >/dev/null 2>&1")
    os.system("chmod 0700 /home/xtreamcodes/iptv_xtream_codes/config > /dev/null")
    os.system("sed -i 's|echo \"Xtream Codes Reborn\";|header(\"Location: https://www.google.com/\");|g' /home/xtreamcodes/iptv_xtream_codes/wwwdir/index.php")
    if not "api.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    api.xtream-codes.com" >> /etc/hosts')
    if not "downloads.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    downloads.xtream-codes.com" >> /etc/hosts')
    if not "xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    xtream-codes.com" >> /etc/hosts')
    if not "@reboot root /etc/init.d/xtreamcodes restart" in open("/etc/crontab").read(): os.system('echo "@reboot root /etc/init.d/xtreamcodes restart" >> /etc/crontab')

def start(first=True):
    if first: 
        printc("Starting Xtream Codes")
        os.system("sudo /etc/init.d/xtreamcodes restart > /dev/null")
    else: 
        printc("Restarting Xtream Codes")
        os.system("sudo /etc/init.d/xtreamcodes restart > /dev/null")

def modifyNginx():
    printc("Modifying Nginx")
    rPath = "/home/xtreamcodes/iptv_xtream_codes/nginx/conf/nginx.conf"
    rPrevData = open(rPath, "r").read()
    if not "listen 25500;" in rPrevData:
        shutil.copy(rPath, "%s.xc" % rPath)
        rData = "}".join(rPrevData.split("}")[:-1]) + "    server {\n        listen 25500;\n        index index.php index.html index.htm;\n        root /home/xtreamcodes/iptv_xtream_codes/admin/;\n\n        location ~ \.php$ {\n			limit_req zone=one burst=8;\n            try_files $uri =404;\n			fastcgi_index index.php;\n			fastcgi_pass php;\n			include fastcgi_params;\n			fastcgi_buffering on;\n			fastcgi_buffers 96 32k;\n			fastcgi_buffer_size 32k;\n			fastcgi_max_temp_file_size 0;\n			fastcgi_keep_conn on;\n			fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;\n			fastcgi_param SCRIPT_NAME $fastcgi_script_name;\n        }\n    }\n}"
        rFile = open(rPath, "w")
        rFile.write(rData)
        rFile.close()

if __name__ == "__main__":
    try: rVersion = os.popen('lsb_release -sr').read().strip()
    except: rVersion = None
    if not rVersion in rVersions:
        printc("Unsupported Operating System, Ubuntu %s" % rVersion, col.GREEN, 2)
        sys.exit(1)
    if rVersion == "20.04":
        rPackages.append("libzip5")
    elif rVersion == "18.04":
        rPackages.append("libzip4")
    else:
        rPackages.append("libzip5")
    printc("XtreamUI 22f Ubuntu %s - Moded XoceUnder" % rVersion, col.GREEN, 2)
    print(" ")
    rType = input("  Installation Type [MAIN, LB, UPDATE]: ")
    print(" ")
    if rType.upper() in ["MAIN", "LB"]:
        if rType.upper() == "LB":
            rHost = input("  Main Server IP Address: ")
            rPassword = input("  MySQL Password: ")
            try: rServerID = int(input("  Load Balancer Server ID: "))
            except: rServerID = -1
            print(" ")
        else:
            rHost = "127.0.0.1"
            rPassword = generate()
            rServerID = 1
        rUsername = generate()
        rDatabase = "xtream_iptvpro"
        rPort = 7999
        if len(rHost) > 0 and len(rPassword) > 0 and rServerID > -1:
            printc("Start installation? Y/N", col.BRIGHT_YELLOW)
            if input("  ").upper() == "Y":
                print(" ")
                rRet = prepare(rType.upper())
                if not install(rType.upper()): sys.exit(1)
                if rType.upper() == "MAIN":
                    if not mysql(rUsername, rPassword): sys.exit(1)
                encrypt(rHost, rUsername, rPassword, rDatabase, rServerID, rPort)
                configure()
                if rType.upper() == "MAIN": 
                    modifyNginx()
                    update(rType.upper())
                start(1)
                printc("Installation completed!", col.GREEN, 2)
                if rType.upper() == "MAIN":
                    printc("Please store your MySQL password: %s" % rPassword, col.BRIGHT_YELLOW)
                    printc("Admin UI Wan IP: http://%s:25500" % getIP(), col.BRIGHT_YELLOW)
                    printc("Admin UI default login is admin/admin", col.BRIGHT_YELLOW)
                    printc("Your mysql credentials have been saved to:")
                    printc("Save Credentials is file to %s/credentials.txt" % rPath, col.BRIGHT_YELLOW)
                    rFile = open(rPath + "/credentials.txt", "w")
                    rFile.write("MySQL Username: %s\nMySQL Password: %s\n" % (rUsername, rPassword))
                    rFile.write("Admin UI Wan IP: http://%s:25500\n" % getIP())
                    rFile.write("Admin UI default login is admin/admin\n")
                    rFile.close()
            else: printc("Installation cancelled", col.BRIGHT_RED)
        else: printc("Invalid entries", col.BRIGHT_RED)
    elif rType.upper() == "UPDATE":
        if os.path.exists("/home/xtreamcodes/iptv_xtream_codes/wwwdir/api.php"):
            printc("Update Admin Panel? Y/N?", col.BRIGHT_YELLOW)
            if input("  ").upper() == "Y":
                if not update(rType.upper()): sys.exit(1)
                printc("Installation completed!", col.GREEN, 2)
                start()
            else: printc("Install Xtream Codes Main first!", col.BRIGHT_RED)
    else: printc("Invalid installation type", col.BRIGHT_RED)
