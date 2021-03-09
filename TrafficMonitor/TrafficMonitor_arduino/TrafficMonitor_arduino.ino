/*
    Three WiFi Meters - Traffic Monitor
    -
    David Chatting - github.com/davidchatting/ThreeWiFiMeters
    MIT License - Copyright (c) March 2021
    Example documented here > https://github.com/davidchatting/Approximate/tree/master#traffic-monitor
*/

#include <YoYoWiFiManager.h>
#include <Approximate.h>
#include <YoYoSettings.h>

YoYoWiFiManager wifiManager;
YoYoSettings *settings;

Approximate approx;

const int ledPin = 16; //DO

List<Device *> activeDevices;
const int maxActiveDevices = 512;

void setup() {
  Serial.begin(115200);

  settings = new YoYoSettings(512); //Settings must be created here in Setup() as contains call to EEPROM.begin() which will otherwise fail
  wifiManager.init(settings, onceConnected, NULL, NULL, false, 80, ledPin, HIGH);

  wifiManager.begin("Home Network Study", "blinkblink");
}

void onceConnected() {
  for(int i=0; i<3; ++i) {
    wifiManager.setWifiLED(HIGH);
    delay(150);
    wifiManager.setWifiLED(LOW);
    delay(150);
  }
  wifiManager.end();
  
  if (approx.init()) {
    approx.setActiveDeviceHandler(onActiveDevice);
    approx.begin();
  }
}

void loop() {
  uint8_t wifiStatus = wifiManager.loop();
  approx.loop();

  if(Serial.available()) {
    serialEvent();
  }
}

void onActiveDevice(Device *device, Approximate::DeviceEvent event) {
  if (activeDevices.Count() >= maxActiveDevices) {
    Device *activeDevice = activeDevices[0];
    activeDevices.Remove(0);
    delete activeDevice;
  }
  activeDevices.Add(new Device(device));
}

void serialEvent() {
  while (Serial.available()) {
    if((char)Serial.read() == 'x') {
      Device *activeDevice = NULL;
      char macAddress[18];
      
      char status[32];
      wifiManager.getStatusAsString(status);

      if(activeDevices.Count() > 0) {
        while (activeDevices.Count() > 0) {
          activeDevice = activeDevices[0];
          
          Serial.printf("[aprx]\t%s\t%s\t%i\t%i\n", status, activeDevice->getMacAddressAs_c_str(macAddress), activeDevice->getUploadSizeBytes(), activeDevice->getDownloadSizeBytes());
          activeDevices.Remove(0);
          delete activeDevice;
        }
      }
      else {
        Serial.printf("[aprx]\t%s\n", status);
      }
    }
  }
}
