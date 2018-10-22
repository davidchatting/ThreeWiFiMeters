#adapted from https://github.com/domsom/NetworkManager-ds/blob/c81179c0449abb3442de4b9fd082bad19e5c23ee/examples/python/show-bssids.py

import dbus

bus = dbus.SystemBus()

# Get a proxy for the base NetworkManager object
proxy = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
manager = dbus.Interface(proxy, "org.freedesktop.NetworkManager")

all_aps = []

device = manager.GetDeviceByIpIface("wlan0")
dev_proxy = bus.get_object("org.freedesktop.NetworkManager", device)
prop_iface = dbus.Interface(dev_proxy, "org.freedesktop.DBus.Properties")

# Make sure the device is enabled before we try to use it
state = prop_iface.Get("org.freedesktop.NetworkManager.Device", "State")
if state <= 2:
    exit(1)

# Get device's type; we only want wifi devices
iface = prop_iface.Get("org.freedesktop.NetworkManager.Device", "Interface")
dtype = prop_iface.Get("org.freedesktop.NetworkManager.Device", "DeviceType")
if dtype == 2:   # WiFi
    # Get a proxy for the wifi interface
    wifi_iface = dbus.Interface(dev_proxy, "org.freedesktop.NetworkManager.Device.Wireless")
    wifi_prop_iface = dbus.Interface(dev_proxy, "org.freedesktop.DBus.Properties")

    # Get the associated AP's object path
    #connected_path = wifi_prop_iface.Get("org.freedesktop.NetworkManager.Device.Wireless", "ActiveAccessPoint")

    # Get all APs the card can see
    aps = wifi_iface.GetAccessPoints()
    for path in aps:
        ap_proxy = bus.get_object("org.freedesktop.NetworkManager", path)
        ap_prop_iface = dbus.Interface(ap_proxy, "org.freedesktop.DBus.Properties")
        bssid = ap_prop_iface.Get("org.freedesktop.NetworkManager.AccessPoint", "HwAddress")
        ssid_dbusArray = ap_prop_iface.Get("org.freedesktop.NetworkManager.AccessPoint", "Ssid")
        ssid = ''.join([chr(byte) for byte in ssid_dbusArray])

        # Cache the BSSID
        if not bssid in all_aps:
            all_aps.append(bssid)
            print(ssid + "\t\t" + bssid)
