#!/usr/bin/env python

import json
import yaml
import pprint

with open("list.json") as j:
    jlist = json.load( j )

print "\nJSON list \n"
pprint.pprint( jlist )

with open("list.yaml") as y:
    ylist = yaml.load( y )

print "\nYAML list\n"
print yaml.dump( ylist )
