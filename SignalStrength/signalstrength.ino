#include <YoYoWiFiManager.h>
#include <YoYoSettings.h>

YoYoWiFiManager wifiManager;
YoYoSettings *settings;

const int gaguePin = 5;
const int ledPin = 12;

const int minRSSI = -80;
const int maxRSSI = -20;

void setup() {
  Serial.begin(115200);

  analogWrite(gaguePin, 255);
  delay(150);
  analogWrite(gaguePin, 0);
  
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
}

void loop() {
  if(wifiManager.loop() == YY_CONNECTED) {
    int32_t rssi = getRSSI(WiFi.SSID());
    if(rssi == 0){
      analogWrite(gaguePin, 0);
    }
    else{
      int valueToDisplay = map(rssi, maxRSSI, minRSSI, 255, 0);
      valueToDisplay = min(max(valueToDisplay, 0), 255);
  
      Serial.print(rssi);
      Serial.print("\t");
      Serial.print(valueToDisplay);
      Serial.print("\n");
      
      analogWrite(gaguePin, valueToDisplay);
    }
  }
  else{
    analogWrite(gaguePin, 0);
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
