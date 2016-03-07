#!/usr/bin/env python

# send an email notification if the RunningLastChange is bigger then StartupLastChanged
# Special case, RunningLastChange is less then 6000 (1 minute), then we can ignore it

import subprocess
from subprocess import Popen, PIPE
from email.mime.text import MIMEText
import socket
import time

import snmp_helper

def sendmail(from_addr, to_addr, subject, message):
    msg = MIMEText( message )
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject
    #smtp_conn = smtplib.SMTP('localhost')
    m = Popen(["/usr/sbin/sendmail", "-t", "-oi", "-f " + from_addr], stdin=PIPE, universal_newlines=True)
    m.communicate(msg.as_string())

    return True

    # Send the email
    smtp_conn.sendmail(from_addr, to_addr, msg.as_string())

    # Close SMTP connection
    smtp_conn.quit()

    return True

IP = '50.76.53.27'
username = 'pysnmp'
auth_key = 'galileo1'
encrypt_key = 'galileo1'

snmp_user = (username, auth_key, encrypt_key)

rtr1 = (IP, 7961)
rtr2 = (IP, 8061)

def add_s( num ):
    if (num > 1):
        return 's '
    else:
        return ' '

def covert_seconds_to_human_time ( ms ):
    seconds = int(ms) / 100
    minutes = seconds / 60
    if (minutes > 0):
        seconds = seconds % 60
    hours = minutes / 60
    if (hours > 0):
        minutes = minutes % 60
    days = hours / 24
    if (days > 0):
        hours = hours % 24
    weeks = days / 7
    if (weeks > 0):
        days = days % 7

    timestr = ''
    if (weeks > 0):
        timestr = str(weeks) + ' week' + add_s(weeks)
    if (days > 0):
        timestr += str(days) + ' day' + add_s(days)
    if (hours > 0):
        timestr += str(hours) + ' hour' + add_s(hours)
    if (minutes > 0):
        timestr += str(minutes) + ' minute' + add_s(minutes)
    if (seconds > 0):
        timestr += str(seconds) + ' second' + add_s(seconds)

    return timestr

def was_config_changed( router, snmp_user ):

    # System up time
    sysUptimeOID = '1.3.6.1.2.1.1.3.0'
    # Uptime when running config last changed
    ccmHistoryRunningLastChanged = '1.3.6.1.4.1.9.9.43.1.1.1.0'   

    # Uptime when running config last saved (note any 'write' constitutes a save)    
    ccmHistoryRunningLastSaved = '1.3.6.1.4.1.9.9.43.1.1.2.0'   

    # Uptime when startup config last saved   
    ccmHistoryStartupLastChanged = '1.3.6.1.4.1.9.9.43.1.1.3.0'

    snmp_data = snmp_helper.snmp_get_oid_v3(router, snmp_user, oid=sysUptimeOID)
    router_uptime = int(snmp_helper.snmp_extract(snmp_data))
#    print 'uptime:  ' + str( router_uptime ) + ': ' + covert_seconds_to_human_time( router_uptime )

    snmp_data = snmp_helper.snmp_get_oid_v3(router, snmp_user, oid=ccmHistoryRunningLastChanged)
    running_last_change_time = int(snmp_helper.snmp_extract(snmp_data))
#    print 'running last change: ' + str( running_last_change_time ) + ' ' + str( router_uptime - running_last_change_time )

    snmp_data = snmp_helper.snmp_get_oid_v3(router, snmp_user, oid=ccmHistoryRunningLastSaved)
    running_last_save_time = int(snmp_helper.snmp_extract(snmp_data))
#    print 'running last save:   ' + str( running_last_save_time ) + ' ' + str( router_uptime - running_last_save_time )

    snmp_data = snmp_helper.snmp_get_oid_v3(router, snmp_user, oid=ccmHistoryStartupLastChanged)
    startup_last_change_time = int(snmp_helper.snmp_extract(snmp_data))
#    print 'startup last change: ' + str( startup_last_change_time ) + ' ' + str( router_uptime - startup_last_change_time )

    if (running_last_change_time > 600 and (running_last_change_time > startup_last_change_time)):
        output = covert_seconds_to_human_time(router_uptime - running_last_change_time) + 'since last change of running config\n'
        output += covert_seconds_to_human_time(router_uptime - startup_last_change_time) + 'since last save of running config\n'
        return output

    return ''



def main():
    output = was_config_changed( rtr1, snmp_user )
    if (output != ''):
#        print '\n-------------'
        print output
        sendmail('kadamski@yorku.ca', 'kadamski@yorku.ca', 'Running configuration on router ' + rtr1[0] + ' was not saved', output)

if __name__ == "__main__":
    main()
