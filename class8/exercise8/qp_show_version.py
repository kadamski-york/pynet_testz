#! /usr/bin/env python


import netmiko
import datetime
import net_system.models
import django
import multiprocessing

def show_version_q( a_device, q ):
    output_list = {}

    output = a_device.device_name + '\n'
    remote_conn = netmiko.ConnectHandler( device_type=a_device.device_type,
                                            ip=a_device.ip_address,
                                            username=a_device.credentials.username,
                                            password=a_device.credentials.password,
                                            port=a_device.port )
    output += remote_conn.send_command( "show version" ) + '\n'
    output_list[a_device.device_name] = output
    q.put( output_list )

def main():
    django.setup()
    p_list = []
    q = multiprocessing.Queue( maxsize=20 )

    devices = net_system.models.NetworkDevice.objects.all()
    start_time = datetime.datetime.now()
    for a_device in devices:
        a_process = multiprocessing.Process( target=show_version_q, args=(a_device, q) )
        a_process.start()
        p_list.append( a_process )

    for p in p_list:
        p.join()
        print
        print '*' * 80
        out_dic = q.get()
        for k,v in out_dic.iteritems():
            print v

    end_time = datetime.datetime.now()

    print
    print '*' * 80
    print 'Run time: ', end_time - start_time

if __name__ == "__main__":
    main()
