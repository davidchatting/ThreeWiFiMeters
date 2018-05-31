#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <WiFiManager.h>         //https://github.com/tzapu/WiFiManager

void setup() {
  Serial.begin(9600);

  WiFiManager wifiManager;
  wifiManager.autoConnect("Signal Strength Meter"); //blocks waiting for wifi to be configured
}

void loop() {
  //if (WiFi.status() == WL_CONNECTED) {
    int32_t rssi = getRSSI(WiFi.SSID());
    if(rssi==0){
      analogWrite(5, 0);
    }
    else{
      int valueToDisplay = map(rssi, 0, -100, 50, 0);
  
      Serial.print(rssi);
      Serial.print("\t");
      Serial.print(valueToDisplay);
      Serial.print("\n");
      
      analogWrite(5, valueToDisplay);
    }
  //}
}

// Return RSSI or 0 if target SSID not found
int32_t getRSSI(String target_ssid) {
  byte available_networks = WiFi.scanNetworks();

  for (int network = 0; network < available_networks; network++) {
    if (WiFi.SSID(network).equals(target_ssid)) {    
      return WiFi.RSSI(network);
    }
  }
  return 0;
}
