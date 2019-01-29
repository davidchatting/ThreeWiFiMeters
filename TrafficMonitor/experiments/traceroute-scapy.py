import scapy.all
import socket
import time

import ipaddress
import pings
Ping = pings.Ping()

def ping(ipAddress):
    delayMs = -1    

    print("ping *" + ipAddress + "*")

    response = Ping.ping(ipAddress, times=3)

    response.print_messages()
    
    return delayMs

# # The fastest way to discover hosts on a local ethernet network is to use the ARP Ping method:
# ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=host), timeout=2)

# # Answers can be reviewed with the following command:
# ans.summary(lambda s, r: r.sprintf("%Ether.src% %ARP.psrc%"))

def ping(ipAddress,depth):
    pkt = scapy.all.IP(dst = ipAddress, ttl = depth) / scapy.all.UDP(dport=33434)
    # Send the packet and get a reply
    reply = scapy.all.sr1(pkt, verbose=0, timeout=2)

    if reply is not None:
        delayMs = int(round((reply.time - pkt.time) * 1000))
        print(depth, delayMs, reply.src)
    else:
        print('*')

    return reply

def locateNetwork():
    localRouter = ""
    internetGateway = ""
    remoteServer = "91.146.107.101"   #www.davidchatting.com use ip address so get more info if DNS is unreachable
    try:
        for i in range(1, 28):
            reply = ping(remoteServer,depth = i)

            if reply is not None:
                if len(localRouter) == 0:
                    localRouter = reply.src
                
                if len(internetGateway) == 0 and not ipaddress.ip_address(reply.src).is_private:
                    internetGateway = reply.src

                #delayMs = int(round((reply.time - pkt.time) * 1000))
                #print(str(i) + ": " + str(delayMs) + " ms " + reply.src + " " + str(ipaddress.ip_address(reply.src).is_private))
                if reply.type == 3:
                    # We've reached our destination
                    break
    except socket.gaierror:
        print("can't resolve hostname")

    # print(ping(localRouter))
    # print(ping(internetGateway))
    # print(ping(remoteServer))

ping("91.146.107.101", depth = 255)
ping("91.146.107.101", depth = 1)
ping("91.146.107.101", depth = 4)
ping("31.55.185.188", depth = 255)

#locateNetwork()