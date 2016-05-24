#! /usr/bin/env python

import time
import paramiko
import socket
import sys
import string
import pexpect

MBUFF = 65535

def login( ip_addr, user, port, ass ):
    try:
        s_connect = pexpect.spawn( 'ssh -l {} {} -p {}'.format( user, ip_addr, port ) )
    except socket.timeout:
        return 0

    s_connect.timeout = 5
    s_connect.expect( 'assword:' )
    s_connect.sendline( ass )
    s_connect.expect( '#' )
    s_connect.sendline( 'terminal length 0' )
    s_connect.expect( '#' )
    return s_connect

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

    ssh_c = login( pynet_rtr2, username, pynet_rtr2_port, password )
    if ssh_c == 0 :
        return

    ssh_c.sendline( 'show ip int brief' );
    ssh_c.expect( '#' )
    print ssh_c.before


if __name__ == "__main__":
    main()
