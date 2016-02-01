#!/usr/bin/env python

from snmp_helper import snmp_get_oid,snmp_extract

OID_sysDescr = '1.3.6.1.2.1.1.1.0'
OID_sysName = '1.3.6.1.2.1.1.5.0'

COMMUNITY_STRING = 'galileo'
RTR1_SNMP_PORT = 7961
RTR2_SNMP_PORT = 8061
RTR1_IP = '50.76.53.27'
RTR2_IP = '50.76.53.27'

rtr1_device = (RTR1_IP, COMMUNITY_STRING, RTR1_SNMP_PORT)
rtr2_device = (RTR2_IP, COMMUNITY_STRING, RTR2_SNMP_PORT)

def getNameDescr(rtr_device):
    snmp_data = snmp_get_oid(rtr_device, oid=OID_sysName)
    output = snmp_extract(snmp_data) + '\n'
    snmp_data = snmp_get_oid(rtr_device, oid=OID_sysDescr)
    output += snmp_extract(snmp_data)
    return output

print getNameDescr(rtr1_device)

print '\n-------------------------------------------------\n'

print getNameDescr(rtr2_device)

