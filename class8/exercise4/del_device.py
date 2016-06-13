#!/usr/bin/env python

import django
import net_system.models

def delete_device( dev_name ):

    try:
        device = net_system.models.NetworkDevice.objects.get( device_name=dev_name )
        device.delete()
    except:
        pass

def main():

    django.setup()

    delete_device( 'switch-1' )
    delete_device( 'router-2' )

    devices = net_system.models.NetworkDevice.objects.all()

    for a_device in devices:
        print a_device.device_name, a_device.device_type, a_device.ip_address, a_device.port

if __name__ == "__main__":
    main()

