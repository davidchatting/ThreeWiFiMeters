//#include <ESP8266WiFi.h>

//#include <DNSServer.h>
//#include <WiFiManager.h>         //https://github.com/tzapu/WiFiManager

#include <Approximate.h>
Approximate approx;

List<Device *> activeDevices;
const int maxActiveDevices = 512;

void setup() {
  Serial.begin(115200);
  
//  WiFiManager wifiManager;  
//  wifiManager.autoConnect("Traffic Monitor"); //blocks waiting for wifi to be configured
//
//  if (approx.init()) {
//    approx.setActiveDeviceHandler(onActiveDevice);
//    approx.start();
//  }

  if (approx.init("HackMyHouse", "loveofmoney")) {
      approx.setActiveDeviceHandler(onActiveDevice);
      approx.begin();
  }
}

void loop() {
  approx.loop();

  if(Serial.available()) serialEvent();
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
      
      while (activeDevices.Count() > 0) {
        activeDevice = activeDevices[0];
        
        Serial.printf("[aprx]\t%s\t%i\t%i\n", activeDevice->getMacAddressAs_c_str(macAddress), activeDevice->getUploadSizeBytes(), activeDevice->getDownloadSizeBytes());
        activeDevices.Remove(0);
        delete activeDevice;
      }
    }
  }
}
