import nmap
import socket
import time

nm = nmap.PortScanner()             # instantiate nmap.PortScanner object

def getsubnet():
    subnet=getipaddress()
    subnet=subnet[:subnet.rfind('.')-len(subnet)]
    return(subnet)

def getipaddress():
    return([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

thisSubnet = getsubnet()
#thisIP = getipaddress()

def mapnetwork():
    while True:
        print('----------------------------------------------------')

        nm.scan(hosts=getsubnet()+'.0/24', arguments='-R -sP -PE -PA21,23,80,3389')  #-O -R -sS -PE -PA21,23,80,3389
        for h in nm.all_hosts():
            ipAddress=nm[h]['addresses']['ipv4']
            print(getDeviceFromIPAddress(ipAddress), ipAddress, nm[h]['vendor'], nm[h].hostname())    #, nm[h]['osclass']
        time.sleep(60)
    return

def getDeviceFromIPAddress(ipAddress):
    result=-1

    if ipAddress.startswith(thisSubnet):
        n=ipAddress[len(thisSubnet)+1:]
        if len(n)>0:
            result=int(n)

    return (result)

mapnetwork()