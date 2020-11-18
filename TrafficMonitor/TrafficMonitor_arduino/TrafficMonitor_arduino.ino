//#include <ESP8266WiFi.h>

//#include <DNSServer.h>
//#include <WiFiManager.h>         //https://github.com/tzapu/WiFiManager

#include <Approximate.h>
Approximate approx;

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
}

void onActiveDevice(Device *device, Approximate::DeviceEvent event) {
  char macAddress[18];
  Serial.printf("[aprx]\t%s\t%i\t%i\n", device->getMacAddressAs_c_str(macAddress), device->getUploadSizeBytes(), device->getDownloadSizeBytes());
}
