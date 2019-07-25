# sudo airmon-ng start wlan1 1

from scapy.all import *

apSSID = "HackMyHouse"
apMacAddress = ""

def PacketHandler(packet) :
	global apMacAddress

	# if packet has 802.11 layer, and type of packet is Data frame
	if packet.haslayer(Dot11):
		#dot11_layer=packet.getlayer(Dot11)

		#data frame:
		if packet.type == 2:
			packet.show()

			#print("{}	{}	{}	{}".format(packet.addr1, packet.addr2, packet.addr3, packet.addr4))
			#print ("dot11_layer.payload length: {}".format(dot11_layer.payload.name))
			# if packet.addr3 == apMacAddress :
				# print("{}	{}".format(packet.addr3, packet.len))

		if packet.type == 0 and packet.subtype == 8 :
			#print(packet.info.decode())

			#print ("AP MAC: {} with SSID: {}".format(packet.addr3, packet.info.decode()))
			if packet.info.decode() == apSSID :
				apMacAddress = packet.addr3

	# if packet.haslayer(Dot11WEP):
	# 	#packet.show()
	# 	print("{}	{}	{}	{}".format(packet.addr1, packet.addr2, packet.addr3, len(packet.wepdata)))

sniff(iface="wlan1mon", prn = PacketHandler, store=0)