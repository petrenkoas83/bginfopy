import os
import netifaces

from preferences import *

def get_ifipv4():
    ifipv4 = []
    for interface in netifaces.interfaces():
        # http://www.programcreek.com/python/example/81993/netifaces.AF_INET
        # list of ipv4 addrinfo dicts
        ipv4 = netifaces.ifaddresses(interface).get(netifaces.AF_INET, [])
        for entry in ipv4:
            addr = entry.get('addr')
            if not addr:
                continue
            if not (interface.startswith('lo') or addr.startswith('127.')):
                ifipv4.append("Interface {0}: {1}".format(interface, addr))
    return ifipv4