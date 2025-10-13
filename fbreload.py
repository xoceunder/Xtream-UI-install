#!/usr/bin/python3
import subprocess, os, sys, base64
from itertools import cycle

rConfigPath = "/home/xtreamcodes/iptv_xtream_codes/config"

def encrypt(rHost="127.0.0.1", rUsername="", rPassword="", rDatabase="xtream_iptvpro", rServerID=1, rPort=7999):
    try: os.remove(rConfigPath)
    except: pass
    rf = open(rConfigPath, 'wb')
    lestring=''.join(chr(ord(c)^ord(k)) for c,k in zip('{\"host\":\"%s\",\"db_user\":\"%s\",\"db_pass\":\"%s\",\"db_name\":\"%s\",\"server_id\":\"%d\", \"db_port\":\"%d\"}' % (rHost, rUsername, rPassword, rDatabase, rServerID, rPort), cycle('5709650b0d7806074842c6de575025b1')))
    rf.write(base64.b64encode(bytes(lestring, 'ascii')))
    rf.close()

def start(): 
    os.system("chown xtreamcodes:xtreamcodes /home/xtreamcodes/iptv_xtream_codes/config")
    os.system("chmod 0700 /home/xtreamcodes/iptv_xtream_codes/config")
    os.system("sudo systemctl restart xtreamcodes")

if __name__ == "__main__":
    rHost = sys.argv[1]
    rPort = int(sys.argv[2])
    rUsername = sys.argv[3]
    rPassword = sys.argv[4]
    rDatabase = sys.argv[5]
    rServerID = int(sys.argv[6])
    encrypt(rHost, rUsername, rPassword, rDatabase, rServerID, rPort)
    start()