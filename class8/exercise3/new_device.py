#!/usr/bin/env python

import django
import net_system.models

def main():

    django.setup()

    device_1 = net_system.models.NetworkDevice( device_name='switch-1', device_type='arista_eos', ip_address='10.20.30.40', port=1234, )
    device_1.save()

    device_2 = net_system.models.NetworkDevice( device_name='router-2', device_type='cisco_ios', ip_address='11.21.31.41', port=4321, )
    device_2.save()

    devices = net_system.models.NetworkDevice.objects.all()

    for a_device in devices:
        print a_device.device_name, a_device.device_type, a_device.ip_address, a_device.port

if __name__ == "__main__":
    main()

