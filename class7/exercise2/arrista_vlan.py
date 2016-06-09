#!/usr/bin/env python

import sys
import pyeapi

def print_usage() :
    print "Usage:",
    print sys.argv[0],
    print "{--remove <vlan id> | --name <vlan name> <vlan id>}"
    exit( 0 )

def validate_args() :

    if len( sys.argv ) < 3 :
        print_usage()

    if len( sys.argv ) == 3 :
        if sys.argv[1] == '--remove' :
            if sys.argv[2].isdigit() :
                return 'R'
            else:
                print_usage()
        else:
            print_usage()

    if len( sys.argv ) == 4 :
        if sys.argv[1] == '--name' :
            if sys.argv[3].isdigit() :
                return 'N'

    print_usage()

def vlan_exists( conn, vlan_id ):

    out = conn.enable( 'show vlan' )

    return str( vlan_id ) in out[0]['result']['vlans']

def remove_vlan( conn, vlan_id ) :

    print 'Vlan ' + str( vlan_id ),

    if vlan_exists( conn, vlan_id ) :
        cmd = 'no vlan ' + str( vlan_id )
        out = conn.config( [cmd] )
        print 'removed'
    else:
        print 'does not exist'

def add_vlan( conn, vlan_id, vlan_name ) :

    print 'Vlan ' + str( vlan_id ),
    if vlan_exists( conn, vlan_id ) :
        print 'exists already'
    else:
        cmd = ['vlan ' + str( vlan_id )]
        cmd.append( 'name ' + vlan_name )
        out = conn.config( cmd )
        print 'added'

def main() :

    action = validate_args()

    conn = pyeapi.connect_to( 'pynet-sw2' )
    if action == 'R' :
        vlan_id = sys.argv[2]
        remove_vlan( conn, vlan_id )
    else:
        vlan_name = sys.argv[2]
        vlan_id = sys.argv[3]
        add_vlan( conn, vlan_id, vlan_name )

if __name__ == "__main__" :
    main()
