#! /usr/bin/env python

import time
import paramiko
import socket
import sys
import string

MBUFF = 65535

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

def send_command( router, command ):
    router.send( command.rstrip() + '\n' )
    time.sleep( 1 )
    if router.recv_ready() :
        out = router.recv( MBUFF )
        out = string.replace( out, command.rstrip(), '' )
        return out.lstrip()

    return ''

def empty_readahead( conn ) :
    if conn.recv_ready() :
        return conn.recv( MBUFF )
    return ''

def set_pagging( conn, plen=0 ) :
    conn.send( 'term len '+str( plen )+'\n' )
    time.sleep( 1 )
    empty_readahead( conn )

def main():
    pynet_rtr1 = '50.76.53.27'
    pynet_rtr1_port = 22
    pynet_rtr2 = '50.76.53.27'
    pynet_rtr2_port = 8022
    pynet_jnpr_srx1 = '50.76.53.27'
    pynet_jnpr_srx1_port = 9822
    username = 'pyclass'
    password = '88newclass'

    peramiko_connection = paramiko.SSHClient()
    peramiko_connection.load_system_host_keys()

    peramiko_connection.connect( pynet_rtr2, port=pynet_rtr2_port, username=username, password=password, look_for_keys=False, allow_agent=False )

    MyConnection = peramiko_connection.invoke_shell()

    if MyConnection == 0:
        sys.exit("Connection failed: timeout")

    time.sleep( 2 )
    empty_readahead( MyConnection )
    set_pagging( MyConnection, 0 )

    out = send_command( MyConnection, "configure t" )
    out = send_command( MyConnection, "logging buffer 8196" )
    out = send_command( MyConnection, "end" )

    print out


if __name__ == "__main__":
    main()
