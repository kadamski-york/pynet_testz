#!/usr/bin/env python

import pyeapi

def main():

    conn = pyeapi.connect_to( "pynet-sw2" )

    result = conn.enable( "show interfaces" )

    interfaces = result[0]['result']['interfaces']

    for int in interfaces.keys():
        print int,
        if 'interfaceCounters' in interfaces[int] :
            print '\tInOctets: ',
            print interfaces[int]['interfaceCounters']['inOctets'],
            print '\tOutOctets: ',
            print interfaces[int]['interfaceCounters']['outOctets']
        else:
            print '\tNo counters'

if __name__ == '__main__':
    main()

