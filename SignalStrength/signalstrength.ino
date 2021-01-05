#include <YoYoWiFiManager.h>
#include <YoYoSettings.h>

YoYoWiFiManager wifiManager;
YoYoSettings *settings;

const int gaguePin = 5;
const int ledPin = 12;
const int ledLevel = 64;

const int minRSSI = -100;
const int maxRSSI = -20;

void setup() {
  pinMode(ledPin, OUTPUT);
  analogWrite(ledPin, ledLevel);
  
  Serial.begin(115200);
  
  settings = new YoYoSettings(512); //Settings must be created here in Setup() as contains call to EEPROM.begin() which will otherwise fail
  wifiManager.init(settings);

  wifiManager.begin("Home Network Study", "blinkblink");
}

void loop() {
  if(wifiManager.loop() == YY_CONNECTED) {
    int32_t rssi = getRSSI(WiFi.SSID());
    if(rssi == 0){
      analogWrite(ledPin, ledLevel);
      analogWrite(gaguePin, 0);
    }
    else{
      analogWrite(ledPin, 0);
      
      int valueToDisplay = map(rssi, maxRSSI, minRSSI, 255, 0);
      valueToDisplay = min(max(valueToDisplay, 0), 255);
  
      Serial.print(rssi);
      Serial.print("\t");
      Serial.print(valueToDisplay);
      Serial.print("\n");
      
      analogWrite(gaguePin, valueToDisplay);
    }
  }
}

// Return RSSI or 0 if target SSID not found
int32_t getRSSI(String target_ssid) {
  int32_t result = 0;
  
  byte available_networks = WiFi.scanNetworks();

  for (int network = 0; network < available_networks && result == 0; network++) {
    if (WiFi.SSID(network).equals(target_ssid)) {
      result = WiFi.RSSI(network);
    }
  }
  return(result);
}
