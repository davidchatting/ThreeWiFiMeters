# <img src="TrafficMonitor-icon.svg" height=80px> Traffic Monitor
See the traffic on your home WiFi network with this Traffic Monitor.

<img src="TrafficMonitor-display.gif" height=304px>

## Hardware
* Wemos D1 mini ESP8266 
* Raspberry Pi Zero - https://shop.pimoroni.com/products/raspberry-pi-zero-wh-with-pre-soldered-header
* Waveshare 4 inch Raspberry Pi Display - https://www.waveshare.com/wiki/4inch_RPi_LCD_(A)
* 3mm blue LED
* 1K Ohm resistor
* Micro USB male to Micro USB female charge + data adapter cable

<img src="TrafficMonitor-circuit.png" width=600px>

The circuit shows a Wemos D1 mini ESP8266, but the code will compile for any ESP8266 or ESP32 (pin assignments will need to change of course).

## Software
### Arduino
The Arduino core for the ESP8266 or ESP32 must be installed:
* ESP8266 - https://github.com/esp8266/Arduino#installing-with-boards-manager
* ESP32 - https://github.com/espressif/arduino-esp32/blob/master/docs/arduino-ide/boards_manager.md

And following Arduino libraries are required:
* Approximate - https://github.com/davidchatting/Approximate/
* YoYoWiFiManager - https://github.com/interactionresearchstudio/YoYoWiFiManager
* ListLib - https://github.com/luisllamasbinaburo/Arduino-List

### Processing
https://github.com/gohai/processing-uploadtopi