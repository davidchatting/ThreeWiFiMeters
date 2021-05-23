# <img src="TrafficMonitor-icon.svg" height=80px> Traffic Monitor
See the traffic on your home WiFi network with this Traffic Monitor. Once the WiFi is configured by joining the "Home Network Study" network and setting the credentials via the captive portal, the last three minutes of network traffic will be displayed. The devices on the network are shown on the periphery of the circle and flash when they are active.

<img src="TrafficMonitor-display.gif" height=304px>

## Hardware
The ESP8266 monitors the network traffic and communicates over a serial connection with the Raspberry Pi, which renders the visualisation.

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
The visulisation code is built for [Processing 3](https://processing.org/) from a desktop this can be easily uploaded to the Raspberry Pi using the [Upload to Pi Tool](https://github.com/gohai/processing-uploadtopi). Alternatively, if the ESP8266 is attached to the desktop machine via USB then it can be run there instead - for some platforms other than MacOS that might need some modifcation of ```looksLikeArduino()``` in the sketch.