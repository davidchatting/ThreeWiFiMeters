import scapy.all
import socket
import time
import pyspeedtest

def nowMs():
    return(int(round(time.time() * 1000)))

st = pyspeedtest.SpeedTest()
st.download()

target = "91.146.107.101"   #www.davidchatting.com use ip address so get more info if DNS is unreachable
try:
    for i in range(1, 28):
        pkt = scapy.all.IP(dst=target, ttl=i) / scapy.all.UDP(dport=33434)
        # Send the packet and get a reply
        timeSentMs = nowMs()
        reply = scapy.all.sr1(pkt, verbose=0, timeout=2)

        if reply is not None:
            delayMs = nowMs() - timeSentMs
            print(str(i) + ": " + str(delayMs) + " ms " + reply.src)
            if reply.type == 3:
                # We've reached our destination
                break
except socket.gaierror:
    print("can't resolve hostname")