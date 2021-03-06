#! /usr/bin/env python

import time
import paramiko
import socket
import sys
import string
from netmiko import ConnectHandler
import netmiko

def main():
    username = 'pyclass'
    password = '88newclass'
    pynet1 = {
        'device_type': 'cisco_ios',
        'ip': '50.76.53.27',
        'username': username,
        'password': password,
        'port': 22,
    }
    pynet2 = {
        'device_type': 'cisco_ios',
        'ip': '50.76.53.27',
        'username': username,
        'password': password,
        'port': 8022,
    }
    juniper_srx = {
        'device_type': 'juniper',
        'ip': '50.76.53.27',
        'username': username,
        'password': password,
        'secret': '',
        'port': 9822,
    }


    pynet_rtr2 = ConnectHandler( **pynet2 )

    pynet_rtr2.config_mode()

    if pynet_rtr2.check_config_mode() :
        print "We are in config mode for pynet rtr2"
    else:
        print "No config mode for pynet rtr2"


if __name__ == "__main__":
    main()
