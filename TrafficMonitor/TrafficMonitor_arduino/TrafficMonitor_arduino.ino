/*
    Three WiFi Meters - Traffic Monitor
    -
    David Chatting - github.com/davidchatting/ThreeWiFiMeters
    MIT License - Copyright (c) March 2021
    Documented here > https://github.com/davidchatting/ThreeWiFiMeters#-traffic-monitor
*/

#include <YoYoWiFiManager.h>
#include <Approximate.h>
#include <YoYoSettings.h>

YoYoWiFiManager wifiManager;
YoYoSettings *settings;

Approximate approx;

const int ledPin = 16; //DO

List<Device *> activeDevices;
const int maxActiveDevices = 64;
const int minPayloadSizeBytes = 64;
char status[32];

void setup() {
  Serial.begin(115200);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  settings = new YoYoSettings(512); //Settings must be created here in Setup() as contains call to EEPROM.begin() which will otherwise fail
  wifiManager.init(settings, onceConnected, NULL, NULL, false, 80, -1);

  //Attempt to connect to a WiFi network previously saved in the settings, 
  //if one can not be found start a captive portal called "YoYoMachines", 
  //with a password of "blinkblink" to configure a new one:
  wifiManager.begin("Home Network Study", "blinkblink");
  randomSeed(analogRead(0));
}

void onceConnected() {
  wifiManager.end();
  
  if (approx.init("", "", false, false, false)) {
    approx.setActiveDeviceHandler(onActiveDevice);
    approx.begin();
  }
}

void loop() {
  uint8_t wifiStatus = wifiManager.loop();
  approx.loop();

  if(approx.isRunning()) {
    digitalWrite(ledPin, HIGH);
  }
  else {
    switch(wifiManager.currentMode) {
      case YoYoWiFiManager::YY_MODE_PEER_CLIENT:
        digitalWrite(ledPin, blink(1000));
        break;
      default:  //YY_MODE_PEER_SERVER
        digitalWrite(ledPin, blink(500));
        break;
    }
  }

  if(Serial.available()) {
    serialEvent();
  }
}

bool blink(int periodMs) {
  return(((millis() / periodMs) % 2) == 0);
}

void onActiveDevice(Device *device, Approximate::DeviceEvent event) {
  int n = activeDevices.Count();
  if (n <= maxActiveDevices) {
    if(n == 0 || device -> getPayloadSizeBytes() > minPayloadSizeBytes || random(10) == 0) {
      activeDevices.Add(new Device(device));
    }
  }
}

void serialEvent() {
  while (Serial.available()) {
    if((char)Serial.read() == 'x') {
      wifiManager.getStatusAsString(status);

      if(activeDevices.Count() > 0) {
        char macAddress[18];
 
        while (activeDevices.Count() > 0) {
          Device *activeDevice = activeDevices[0];
          
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
