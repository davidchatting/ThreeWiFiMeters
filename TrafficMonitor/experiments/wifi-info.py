import NetworkManager as NM
import time

def utils_wifi_freq_to_channel(mhz):
	return {
		2412: 1,
		2417: 2,
		2422: 3,
		2427: 4,
		2432: 5,
		2437: 6,
		2442: 7,
		2447: 8,
		2452: 9,
		2457: 10,
		2462: 11,
		2467: 12,
		2472: 13,
		2484: 14,
		5180: 36,
		5190: 38,
		5200: 40,
		5210: 42,
		5220: 44,
		5230: 46,
		5240: 48,
		5260: 52,
		5280: 56,
		5300: 60,
		5320: 64
	}.get(mhz)

connection = NM.NetworkManager.GetDeviceByIpIface('wlan0')
scanner = NM.NetworkManager.GetDeviceByIpIface('wlan1')

homeSSID = connection.ActiveAccessPoint.Ssid

try:
	scanner.RequestScan({})
	allAccessPoints = scanner.GetAllAccessPoints()	#returns array of NetworkManager.AccessPoint objects
	allAccessPoints.sort(key=lambda ap: ap.Strength, reverse=True)

	for ap in allAccessPoints:
		#potentially more than one match (wifi repeaters 2.4 vs 5g networks etc)
		if ap.Ssid == homeSSID:
			info = {
				'ssid': ap.Ssid,
				'frequency': ap.Frequency,
				'channel': utils_wifi_freq_to_channel(ap.Frequency),
				'level': ap.Strength,
				'HwAddress': ap.HwAddress
			}
			print(info)
except:
	print("probably scanned too soon")