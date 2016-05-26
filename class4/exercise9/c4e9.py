#! /usr/bin/env python

import time
import paramiko
import socket
import sys
import string
from netmiko import ConnectHandler
import netmiko
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
import multiprocessing
import datetime

def print_output(results):
    
    print "\nSuccessful devices:"
    for a_dict in results:
        for identifier,v in a_dict.iteritems():
            (success, out_string) = v
            if success:
                print '\n\n'
                print '#' * 80
                print 'Device = {0}\n'.format(identifier)
                print out_string
                print '#' * 80

    print "\n\nFailed devices:\n"
    for a_dict in results:
        for identifier,v in a_dict.iteritems():
            (success, out_string) = v
            if not success:
                print 'Device failed = {0}'.format(identifier)

    print "\nEnd time: " + str( datetime.datetime.now() )
    print

def show_arp( a_device, mp_queue ) :

    identifier = '{ip}:{port}'.format( **a_device )
    return_data = {}

    cmd = 'show arp'
    SSHClass = netmiko.ssh_dispatcher( a_device['device_type'] )

    try:
        net_connect = SSHClass( **a_device )
        output = net_connect.send_command( cmd )
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        return_data[identifier] = (False, e)

        # Add data to the queue (for parent process)
        mp_queue.put( return_data )
        return None

    return_data[identifier] = (True, output )
    mp_queue.put( return_data )

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
        'port': 9822,
    }


    routers = [ pynet1, pynet2, juniper_srx ]

    mp_queue = multiprocessing.Queue()
    processes = []

    print "\nStart time: " + str( datetime.datetime.now() )

    for rtr in routers:
        p = multiprocessing.Process( target=show_arp, args=( rtr, mp_queue ) )
        processes.append( p )
        p.start()

    for p in processes:
        p.join()

    results = []
    for p in processes:
        results.append( mp_queue.get() )

    print_output( results )


if __name__ == "__main__":
    main()
