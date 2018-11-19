import sys
import os
from scapy.all import sr1,IP,ICMP

if len(sys.argv) != 2:
    sys.exit('Usage: traceroute.py <remote host>')

# we start with 1
ttl = 1
while 1:
    p=sr1(IP(dst=sys.argv[1],ttl=ttl)/ICMP(id=os.getpid()), verbose=0)
    # if time exceeded due to TTL exceeded
    if p[ICMP].type == 11 and p[ICMP].code == 0:
        print ttl, '->', p.src
        ttl += 1
    elif p[ICMP].type == 0:
        print ttl, '->', p.src
        break
