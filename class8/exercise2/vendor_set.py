#!/usr/bin/env python

import django
import net_system.models

def main():

    django.setup()

    creds = net_system.models.Credentials.objects.all()

    devices = net_system.models.NetworkDevice.objects.all()

    std_creds = creds[0]
    arista_creds = creds[1]

    for a_device in devices:
        if 'pynet-sw' in a_device.device_name:
            a_device.vendor = 'arista'
        elif 'pynet-rtr' in a_device.device_name:
            a_device.vendor = 'cisco'
        elif 'juniper' in a_device.device_name:
            a_device.vendor = 'juniper'
        a_device.save()

    for a_device in devices:
        print a_device.device_name, a_device.vendor

if __name__ == "__main__":
    main()

"""
pynet-rtr1 pyclass
pynet-rtr2 pyclass
pynet-sw1 admin1
pynet-sw2 admin1
pynet-sw3 admin1
pynet-sw4 admin1
juniper-srx pyclass
"""
