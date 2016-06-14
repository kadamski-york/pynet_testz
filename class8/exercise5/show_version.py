#! /usr/bin/env python


import netmiko
import datetime
import net_system.models
import django

def main():
    django.setup()

    devices = net_system.models.NetworkDevice.objects.all()
    start_time = datetime.datetime.now()
    for a_device in devices:
        print a_device.device_name
        remote_conn = netmiko.ConnectHandler( device_type=a_device.device_type,
                                                ip=a_device.ip_address,
                                                username=a_device.credentials.username,
                                                password=a_device.credentials.password,
                                                port=a_device.port )
        print remote_conn.send_command( "show version" )
        print '=' * 80

    end_time = datetime.datetime.now()

    print
    print '*' * 80
    print 'Run time: ', end_time - start_time

if __name__ == "__main__":
    main()
