//Sniffing code based on Kosme and Ray Burnette's work > https://www.hackster.io/kosme/esp8266-sniffer-9e4770

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <WiFiManager.h>         //https://github.com/tzapu/WiFiManager
#include <EEPROM.h>


// Expose Espressif SDK functionality
extern "C" {
#include "user_interface.h"
  typedef void (*freedom_outside_cb_t)(uint8 status);
  int  wifi_register_send_pkt_freedom_cb(freedom_outside_cb_t cb);
  void wifi_unregister_send_pkt_freedom_cb(void);
  int  wifi_send_pkt_freedom(uint8 *buf, int len, bool sys_seq);
}

const int rssiProximateThreshold = -30;
String pairedMacAddress;

const int sampleIntervalMs = 250;
int nextSampleDueMs = 0;
const int motorPinA = 4;
const int motorPinB = 5;
const int ledPin = 2;     

const int minSpeed = 250;

int bytesRunningTotal = 0;

void promisc_cb(uint8_t *buf, uint16_t len) {
  if (len == 12) {
    //Control frame
  }
  else if (len == 128) {
    //Management frame
  }
  else {
    //Data frame
    //struct sniffer_buf *sniffer = (struct sniffer_buf*) buf;

    int rssi = int8_t(buf[0]);

    String originMacAddress = "";
    for(int i=0;i<6;i++) {
      originMacAddress += String(buf[22+i], HEX);
    }
    
    String destinationMacAddress = "";
    for(int i=0;i<6;i++) {
      destinationMacAddress += String(buf[16+i], HEX);
    }

    if(rssi > rssiProximateThreshold) {
      digitalWrite(ledPin, HIGH);
      if(pairedMacAddress != originMacAddress) {
        pairedMacAddress = originMacAddress;
        Serial.println(pairedMacAddress);
        
        for (int i = 0; i < 12; i++) {
          uint8_t c = pairedMacAddress.charAt(i);
          EEPROM.write(0 + (i * sizeof(uint8_t)), c);
        }
        EEPROM.commit();
      }
    }

    if(len > 60) Serial.println(len);

    //if(len > 60) {
      if(originMacAddress == pairedMacAddress) {
        bytesRunningTotal += len;
      }
      else if(destinationMacAddress == pairedMacAddress) {
        bytesRunningTotal -= len;
      }
    //}
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println("Device Wheel");

  WiFiManager wifiManager;
  wifiManager.autoConnect("Device Wheel"); //blocks waiting for wifi to be configured - just used to set the channel number of this network
  Serial.print("Channel: ");
  Serial.println(wifi_get_channel());

  wifi_set_opmode(STATION_MODE);  //Promiscuous works only with station mode
  wifi_promiscuous_enable(0);     //disable
  wifi_set_promiscuous_rx_cb(promisc_cb);   //Set up promiscuous callback
  wifi_promiscuous_enable(1);     //enable

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);     //lights on LOW

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  
  pinMode(motorPinA, OUTPUT);
  pinMode(motorPinB, OUTPUT);
  setMotorSpeed(0);

  EEPROM.begin(512);
  String s;
  for (int i = 0; i < 12; i++) {
    uint8_t c = EEPROM.read(0 + (i * sizeof(uint8_t)));
    s += (char)c;
  }
  pairedMacAddress = s;
  Serial.print("pairedMacAddress: ");
  Serial.println(pairedMacAddress);

  
  digitalWrite(LED_BUILTIN, HIGH);     //lights on LOW
  digitalWrite(ledPin, LOW);
}

void loop() {
    unsigned long now = millis();
    if(now > nextSampleDueMs) {
      setMotorSpeed(bytesRunningTotal * 1.0f);
      bytesRunningTotal = 0;
      
      nextSampleDueMs = now + sampleIntervalMs;

      digitalWrite(ledPin, LOW);
    }
}

void setMotorSpeed(int v) {
  v = constrain(v, -1024, 1024);
  
  float valueA = 0;
  float valueB = 0;

  if(v != 0) {
    if(v > 0) {
      valueA = v;
      valueB = 0;
  
      digitalWrite(motorPinA, HIGH);
      digitalWrite(motorPinB, LOW);
    }
    else {
      valueA = 0;
      valueB = abs(v);
  
      digitalWrite(motorPinA, LOW);
      digitalWrite(motorPinB, HIGH);
    }
    delay(25);
  }
  
  analogWrite(motorPinA, valueA);
  analogWrite(motorPinB, valueB);
}
