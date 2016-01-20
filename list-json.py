#!/usr/bin/env python

import json

jlist = range(5,76,6)
jlist.append( ("North","South","East","West") )
jlist.append( ["10.5.6.7","192.168.0.0","172.16.0.0"] )
jlist.append( {"Alpha":1, "Beta":2, "Omega":7, "Gama":9} )

print jlist

with open("list.json", "w") as j:
    json.dump( jlist, j )
