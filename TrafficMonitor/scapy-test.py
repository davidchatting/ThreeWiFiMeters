# sudo iw phy phy1 interface add mon1 type monitor
# sudo iw dev wlan1 del
# sudo iw dev mon1 set channel 11
# sudo ifconfig mon1 up

from scapy.all import *

apSSID = "BTHub4-W3MZ"
apMacAddress = ""

def PacketHandler(packet) :
	global apMacAddress

	# if packet has 802.11 layer, and type of packet is Data frame
	if packet.haslayer(Dot11):
		# if packet.type == 2:
		# 	if packet.addr3 == apMacAddress :
		# 		print("{}	{}".format(packet.addr3, packet.len))
		# 		#packet.show()

		if packet.type == 0 and packet.subtype == 8 :
			#print ("AP MAC: {} with SSID: {}".format(packet.addr3, packet.info.decode()))
			if packet.info.decode() == apSSID :
				apMacAddress = packet.addr3

	if packet.haslayer(Dot11WEP):
		# print("{}	{}	{}".format(packet.addr1, packet.addr2, packet.addr3))
		#if packet.addr2 == apMacAddress :
		print(len(packet.wepdata))

sniff(iface="mon1", prn = PacketHandler, store=0)