# Three WiFi Meters
The Three WiFi Meters are three ways of experiencing WiFi networks, each attempts to disclose properties of this near ubiquitous technology. They are built for the [ESP8266](https://en.wikipedia.org/wiki/ESP8266) or [ESP32](https://en.wikipedia.org/wiki/ESP32) using the [Approximate](https://github.com/davidchatting/Approximate) and [YoYoWiFiManager](https://github.com/interactionresearchstudio/YoYoWiFiManager) Arduino libraries.

## <img src="SignalStrength/SignalStrength-icon.svg" height=80px> Signal Strength
Measure the signal strength of your router around the house with the [Signal Strength Meter](SignalStrength).

## <img src="DeviceWheel/DeviceWheel-icon.svg" height=80px> Device Wheel
Watch an individual device's use of the network with the [Device Wheel](DeviceWheel).

## <img src="TrafficMonitor/TrafficMonitor-icon.svg" height=80px> Traffic Monitor
See the traffic on your home WiFi network with the [Traffic Monitor](TrafficMonitor).

## Limitations
The meters works with 2.4GHz WiFi networks, but not 5GHz networks - as neither ESP8266 or ESP32 support this technology.

## Author
The Three WiFi Meters were created by David Chatting ([@davidchatting](https://twitter.com/davidchatting)) as part of the [A Network of One's Own](http://davidchatting.com/nooo/) project. This code is licensed under the [MIT License](LICENSE.txt).