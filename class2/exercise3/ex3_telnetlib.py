#!/usr/bin/env python
'''
Write a script that connects to the lab pynet-rtr1, logins, and executes the
'show ip int brief' command.
'''

import telnetlib
import time
import socket
import sys
import getpass

TELNET_PORT = 23
TELNET_TIMEOUT = 6

class Router:
    timeout = TELNET_TIMEOUT
    port = TELNET_PORT

    def __init__(self, ipaddr, username, password):
        self.ipaddr = ipaddr
        self.username = username
        self.password = password
        self.logindone = 0
        self.output = ''
        try:
            self.connection = telnetlib.Telnet(self.ipaddr, self.port, self.timeout)
        except socket.timeout:
            sys.exit("Connection timed-out")
        except socket.error:
            sys.exit("[Errno 22] Invalid argument")
        except:
            sys.exit("Something unexcepted happened.")

    def login(self):
        '''
        Login to network device
        '''
        self.output = self.connection.read_until("sername", self.timeout)
        self.connection.write(self.username + '\n')
        self.output += self.connection.read_until("assword", self.timeout)
        self.connection.write(self.password + '\n')
        self.logindone = 1
        return self.output

    def disable_paging(self):
        '''
        Disable the paging of output (i.e. --More--)
        '''

        time.sleep(1)
        self.connection.read_very_eager()
        return self.send_command('terminal length 0')

    def send_command(self, cmd):
        '''
        Send a command down the telnet channel

        Return the response
        '''
        cmd = cmd.rstrip()
        self.connection.write(cmd + '\n')
        time.sleep(1)
        return self.connection.read_very_eager()

    def close(self):
        return self.connection.close()

def main():
    '''
    Write a script that connects to the lab pynet-rtr1, logins, and executes the
    'show ip int brief' command.
    '''
    ip_addr = raw_input("IP address: ")
    ip_addr = ip_addr.strip()
    username = 'pyclass'
    password = getpass.getpass()

    router = Router(ip_addr, username, password)
    output = router.login()

    router.disable_paging()

    output = router.send_command('show ip int brief')

    print "\n\n"
    print output
    print "\n\n"

    router.close()

if __name__ == "__main__":
    main()
