// by Ray Burnette 20161013 compiled on Linux 16.3 using Arduino 1.6.12
//Hacked by Kosme 20170520 compiled on Ubuntu 14.04 using Arduino 1.6.11

#include <ESP8266WiFi.h>
#include "./functions.h"

#define disable 0
#define enable  1
unsigned int channel = 6;

void setup() {
  Serial.begin(9600);
  Serial.printf("\n\nSDK version:%s\n\r", system_get_sdk_version());
  Serial.println(F("ESP8266 enhanced sniffer by Kosme https://github.com/kosme"));

  wifi_set_opmode(STATION_MODE);            // Promiscuous works only with station mode
  wifi_set_channel(channel);
  wifi_promiscuous_enable(disable);
  wifi_set_promiscuous_rx_cb(promisc_cb);   // Set up promiscuous callback
  wifi_promiscuous_enable(enable);
}

void loop() {
  /*
  channel = 1;
  wifi_set_channel(channel);
  while (true) {
    nothing_new++;                          // Array is not finite, check bounds and adjust if required
    if (nothing_new > 100) {
      nothing_new = 0;
      channel++;
      if (channel == 15) break;             // Only scan channels 1 to 14
      wifi_set_channel(channel);
    }
    delay(1);  // critical processing timeslice for NONOS SDK! No delay(0) yield()
  }
  */
  delay(1);
}
