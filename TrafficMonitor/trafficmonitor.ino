/*
   based on: https://raw.githubusercontent.com/spacehuhn/PacketMonitor/master/esp8266_packet_monitor/esp8266_packet_monitor.ino
*/

#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <WiFiManager.h>         //https://github.com/tzapu/WiFiManager
#include <EEPROM.h>

extern "C" {
#include "user_interface.h"
}

#define ledPin 2       // led pin ( 2 = built-in LED)

unsigned long prevTime   = 0;
unsigned long curTime    = 0;
unsigned long pkts       = 0;
unsigned long no_deauths = 0;
unsigned long deauths    = 0;

unsigned long bytes       = 0;

void setup() {
  Serial.begin(9600);
  
  WiFiManager wifiManager;
  wifiManager.autoConnect("Traffic Monitor"); //joins preconfigured network or waits for wifi to be configured - both block

  String ssid = WiFi.SSID();

  int channel = getChannel(ssid);
  if (channel != -1) {
    Serial.print(ssid);
    Serial.print(" is channel ");
    Serial.println(channel);

    pinMode(ledPin, OUTPUT);

    wifi_set_opmode(STATION_MODE);
    wifi_promiscuous_enable(0);
    WiFi.persistent(false); //otherwise disconnect will erase the SSID and password stored
    WiFi.disconnect();  
    wifi_set_promiscuous_rx_cb(sniffer);
    wifi_set_channel(channel);
    wifi_promiscuous_enable(1);
  }
}

void loop() {
  curTime = millis();

  //every 1000 ms
  if (curTime - prevTime >= 1000) {
    prevTime = curTime;

    if (pkts == 0) pkts = deauths;
    no_deauths = pkts - deauths;

    Serial.println(bytes);

    deauths    = 0;
    pkts       = 0;

    bytes = 0;
  }
}

void sniffer(uint8_t *buf, uint16_t len) {
  pkts++;
  if (buf[12] == 0xA0 || buf[12] == 0xC0) {
    deauths++;
  }

  bytes+=len;
}

int32_t getChannel(String ssidToFind) {
  int result = -1;

  int n = WiFi.scanNetworks(false, true);

  String ssid;
  uint8_t encryptionType;
  int32_t RSSI;
  uint8_t* BSSID;
  int32_t channel;
  bool isHidden;

  for (int i = 0; i < n; i++) {
    if (WiFi.SSID(i).equals(ssidToFind)) {
      WiFi.getNetworkInfo(i, ssid, encryptionType, RSSI, BSSID, channel, isHidden);
      result = channel;
    }
  }

  return (result);
}
