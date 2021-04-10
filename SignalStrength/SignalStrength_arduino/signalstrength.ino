
/*
    Three WiFi Meters - Signal Strength
    -
    David Chatting - github.com/davidchatting/ThreeWiFiMeters
    MIT License - Copyright (c) March 2021
    Documented here > https://github.com/davidchatting/ThreeWiFiMeters#-signal-strength
*/

#include <YoYoWiFiManager.h>
#include <YoYoSettings.h>

YoYoWiFiManager wifiManager;
YoYoSettings *settings;

const int ledPin = 12;
const int gaguePin = 5;

#if defined(ESP32)
  const int gagueChannel = 0;
#endif

const int minRSSI = -80;
const int maxRSSI = -20;

void setup() {
  Serial.begin(115200);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  #if defined(ESP32)
    ledcSetup(gagueChannel, 1000, 8);
    ledcAttachPin(gaguePin, gagueChannel);
  #endif

  digitalWrite(gaguePin, HIGH);
  delay(150);
  digitalWrite(gaguePin, LOW);
  
  settings = new YoYoSettings(512); //Settings must be created here in Setup() as contains call to EEPROM.begin() which will otherwise fail
  wifiManager.init(settings, onceConnected, NULL, NULL, false, 80, -1);

  wifiManager.begin("Home Network Study", "blinkblink");
}

void onceConnected() {
}

void loop() {
  uint8_t wifiStatus = wifiManager.loop();

  switch(wifiStatus) {
    case YY_CONNECTED:
      digitalWrite(ledPin, HIGH);
      displayRSSI();
      break;
    case YY_CONNECTED_PEER_SERVER:
      digitalWrite(ledPin, blink(500));
      digitalWrite(gaguePin, LOW);
      break;
    default:
      digitalWrite(ledPin, blink(1000));
      digitalWrite(gaguePin, LOW);
      break;
  }
}

bool blink(int periodMs) {
  return(((millis() / periodMs) % 2) == 0);
}

void displayRSSI() {
  int32_t rssi = getRSSI(WiFi.SSID());
  if(rssi == 0){
    digitalWrite(gaguePin, LOW);
  }
  else{
    int valueToDisplay = map(rssi, maxRSSI, minRSSI, 255, 0);
    valueToDisplay = min(max(valueToDisplay, 0), 255);
    
    #if defined(ESP32)
      ledcWrite(gagueChannel, valueToDisplay);
    #else
      analogWrite(gaguePin, valueToDisplay);
    #endif
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
