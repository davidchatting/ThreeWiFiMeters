import scapy.all
import socket
# import time

import ipaddress

localRouter = ""
internetGateway = ""
remoteServer = "1.1.1.1"   #use rather than ip address so no DNS resolution required (which obvs needs network)

def ping(ipAddress):
    # print("ping *" + ipAddress + "*")

    result = False

    reply = traceroute(ipAddress,28)
    if reply is not None:
        result = True
    
    return result

def traceroute(ipAddress,depth):
    pkt = scapy.all.IP(dst = ipAddress, ttl = depth) / scapy.all.UDP(dport=33434)
    # Send the packet and get a reply
    reply = scapy.all.sr1(pkt, verbose=0, timeout=2)

    # if reply is not None:
    #     delayMs = int(round((reply.time - pkt.time) * 1000))
    #     print(depth, delayMs, reply.src)

    return reply

def locateNetwork():
    print("locateNetwork")
    global localRouter, internetGateway, remoteServer

    try:
        for i in range(1, 28):
            reply = traceroute(remoteServer,depth = i)

            if reply is not None:
                if len(localRouter) == 0:
                    localRouter = reply.src
                
                # some gateways (at least the BT ones don't reply to direct pings) 
                if len(internetGateway) == 0 and not ipaddress.ip_address(reply.src).is_private and ping(reply.src):
                    internetGateway = reply.src

                if reply.type == 3:
                    # We've reached our destination
                    break
    except socket.gaierror:
        print("can't resolve hostname")

def testNetwork():
    print("testNetwork")
    global localRouter, internetGateway, remoteServer

    if len(localRouter) == 0:
        locateNetwork()
    
    print("localRouter: " + localRouter + " " + str(ping(localRouter)))
    print("internetGateway: " + internetGateway + " " + str(ping(internetGateway)))
    print("remoteServer:    " + remoteServer + "    " + str(ping(remoteServer)))

testNetwork()