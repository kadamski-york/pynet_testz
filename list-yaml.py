#!/usr/bin/env python

import yaml

ylist = range(5,26,3)
ylist.append( {"alpha":1, "Beta":2, "Omega":7} )
ylist.append( ["10.5.6.7","192.168.0.0","172.16.0.0"] )
ylist.append( ("North","South","East","West") )

print ylist

with open("list.yaml", "w") as y:
    y.write( yaml.dump( ylist, default_flow_style=False ) )
