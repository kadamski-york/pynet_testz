#! /usr/bin/env python

import time
import telnetlib
import socket
import sys
import string

T_PORT = 23
T_TIMEOUT = 5

def login(ip_addr, user, ass):
    try:
        r_connect = telnetlib.Telnet(ip_addr, T_PORT, T_TIMEOUT)
    except socket.timeout:
        return 0

    out = r_connect.read_until("sername", T_TIMEOUT)
    r_connect.write(user + '\n')
    out = r_connect.read_until("assword", T_TIMEOUT)
    r_connect.write(ass + '\n')
    send_command(r_connect, 'set terminal length 0')
    return r_connect

def send_command(router, command):
    router.write(command.rstrip() + '\n')
    time.sleep(1)
    out = router.read_very_eager()
    out = string.replace(out, command.rstrip(), '')
    return out.lstrip()

def main():
    ip_addr = '50.76.53.27'
    username = 'pyclass'
    password = '88newclass'
    router = login(ip_addr, username, password)
    if router == 0:
        sys.exit("Connection failed: timeout")

    out = send_command(router, 'show ip interface brief')
    print out

    router.close()

if __name__ == "__main__":
    main()
