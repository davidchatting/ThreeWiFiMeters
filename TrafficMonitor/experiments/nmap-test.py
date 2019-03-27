import nmap
import socket
import time

nm = nmap.PortScanner()             # instantiate nmap.PortScanner object

devices = ["" for x in range(256)]

def getsubnet(ipAddress):
    subnet=ipAddress[:ipAddress.rfind('.')-len(ipAddress)]
    return(subnet)

def getipaddress():
    return([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

def mapnetwork():
    nm.scan(hosts=getsubnet(getipaddress())+'.0/24', arguments='-R -sP -PE -PA21,23,80,3389')  #-O -R -sS -PE -PA21,23,80,3389

    for d in devices:
        d = ""
    for h in nm.all_hosts():
        ipAddress=nm[h]['addresses']['ipv4']
        # print(getDeviceFromIPAddress(ipAddress), nm[h].hostname())    #, nm[h]['osclass']    nm[h]['vendor'], 
        devices[getDeviceFromIPAddress(ipAddress)] = nm[h].hostname()
    return

def getDeviceFromIPAddress(ipAddress):
    result=-1

    thisSubnet = getsubnet(getipaddress())
    if ipAddress.startswith(thisSubnet):
        n=ipAddress[len(thisSubnet)+1:]
        if len(n)>0:
            result=int(n)

    return (result)

while True:
    mapnetwork()
    print('----------------------------------------------------')
    for i, d in enumerate(devices): 
        if len(d) != 0:
            print(i, d)
    time.sleep(60)