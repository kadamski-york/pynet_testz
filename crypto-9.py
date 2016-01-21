#!/usr/bin/env python

from ciscoconfparse import CiscoConfParse

config = CiscoConfParse( "cisco_ipsec.txt" )

crypto_maps = config.find_objects_w_child( parentspec=r"^crypto map", childspec=r"pfs group2" )

for i in crypto_maps:
    print i.text + ":\n"
    for c in i.children:
        print c.text
    print "\n"


exit()
