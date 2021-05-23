# <img src="DeviceWheel-icon.svg" height=80px> Device Wheel
Watch an individual device's use of the network with this Device Wheel. Once the WiFi is configured by joining the "Home Network Study" network and setting the credentials via the captive portal, bringing an IoT device in proximity of the Device Wheel will cause it to pair and the wheel will spin whenever the is network activity - clockwise for downloads, anti-clockwise for uploads.

## Hardware
* Adafruit HUZZAH32 – ESP32 Feather Board - https://www.adafruit.com/product/3405
* 3800 RPM 1.5mm Diameter Shaft 2V DC Motor for Walkman
* 1.5A Mini Speed Control Dual Channel Motor Driver MX1508
* SPDT Mini Power Switch - https://shop.pimoroni.com/products/spdt-mini-power-switch
* 3mm blue LED
* 1K Ohm resistor
* LiPo Battery Pack 3.7V 500mAh - https://shop.pimoroni.com/products/lipo-battery-pack?variant=20429082055
* Micro USB male to Micro USB female charge + data adapter cable

<img src="DeviceWheel-circuit.png" width=600px>

The circuit shows an Adafruit HUZZAH32, but the code will compile for any ESP8266 or ESP32 (pin assignments will need to change of course).

## Software
### Arduino
The Arduino core for the ESP8266 or ESP32 must be installed:
* ESP8266 - https://github.com/esp8266/Arduino#installing-with-boards-manager
* ESP32 - https://github.com/espressif/arduino-esp32/blob/master/docs/arduino-ide/boards_manager.md

And following Arduino libraries are required:
* Approximate - https://github.com/davidchatting/Approximate/
* YoYoWiFiManager - https://github.com/interactionresearchstudio/YoYoWiFiManager
* ListLib - https://github.com/luisllamasbinaburo/Arduino-List