#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <WiFiManager.h>         //https://github.com/tzapu/WiFiManager

const int gaguePin = 5;
const int ledPin = 12;
const int ledLevel = 64;

const int minRSSI = -100;
const int maxRSSI = -10;

void setup() {
  pinMode(ledPin, OUTPUT);
  analogWrite(ledPin, ledLevel);
  
  Serial.begin(9600);

  WiFiManager wifiManager;
  wifiManager.setCustomHeadElement("<style>html{filter: invert(100%); -webkit-filter: invert(100%);}</style>");

  WiFiManagerParameter custom_text("<p>This is just a text paragraph</p>");
  wifiManager.addParameter(&custom_text);
  
  wifiManager.autoConnect("Signal Strength Meter"); //blocks waiting for wifi to be configured
}

void loop() {
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
