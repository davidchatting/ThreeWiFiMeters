#include <YoYoWiFiManager.h>
#include <Approximate.h>
#include <YoYoSettings.h>

YoYoWiFiManager wifiManager;
YoYoSettings *settings;

Approximate approx;

List<Device *> activeDevices;
const int maxActiveDevices = 512;

void setup() {
  Serial.begin(115200);

  settings = new YoYoSettings(512); //Settings must be created here in Setup() as contains call to EEPROM.begin() which will otherwise fail
  wifiManager.init(settings, onConnected);

  wifiManager.begin("Home Network Study", "blinkblink");
}

void onConnected() {
  wifiManager.end();
  
  if (approx.init()) {
    approx.setActiveDeviceHandler(onActiveDevice);
    approx.begin();
  }
}

void loop() {
  wifiManager.loop();
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
