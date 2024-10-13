#!/usr/bin/python3
import subprocess, os, sys, base64
from itertools import cycle

rConfigPath = "/home/xtreamcodes/iptv_xtream_codes/config"

def encrypt(rHost="127.0.0.1", rUsername="user_iptvpro", rPassword="", rDatabase="xtream_iptvpro", rServerID=1, rPort=7999):
    try: os.remove("/home/xtreamcodes/iptv_xtream_codes/config")
    except: pass
    data_to_encrypt = '{\"host\":\"%s\",\"db_user\":\"%s\",\"db_pass\":\"%s\",\"db_name\":\"%s\",\"server_id\":\"%d\", \"db_port\":\"%d\"}' % (rHost, rUsername, rPassword, rDatabase, rServerID, rPort)
    key = cycle(b'5709650b0d7806074842c6de575025b1')
    encrypted_data_bytes = bytes(c ^ k for c, k in zip(data_to_encrypt.encode(), key))
    encrypted_data = base64.b64encode(encrypted_data_bytes).decode().replace('\n', '')
    with open(rConfigPath, 'wb') as rf:
        rf.write(encrypted_data.encode())
        rf.close()

def start(): 
    os.system("chown xtreamcodes:xtreamcodes /home/xtreamcodes/iptv_xtream_codes/config")
    os.system("chmod 777 /home/xtreamcodes/iptv_xtream_codes/config")
    os.system("/home/xtreamcodes/iptv_xtream_codes/start_services.sh")

if __name__ == "__main__":
    rHost = sys.argv[1]
    rPort = int(sys.argv[2])
    rUsername = sys.argv[3]
    rPassword = sys.argv[4]
    rDatabase = sys.argv[5]
    rServerID = int(sys.argv[6])
    encrypt(rHost, rUsername, rPassword, rDatabase, rServerID, rPort)
    start()