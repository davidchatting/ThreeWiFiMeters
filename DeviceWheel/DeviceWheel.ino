
/*
    Three WiFi Meters - Device Wheel
    -
    David Chatting - github.com/davidchatting/ThreeWiFiMeters
    MIT License - Copyright (c) March 2021
    Documented here > https://github.com/davidchatting/ThreeWiFiMeters#-device-wheel
*/

#include <YoYoWiFiManager.h>
#include <Approximate.h>
#include <YoYoSettings.h>

YoYoWiFiManager wifiManager;
YoYoSettings *settings;

Approximate approx;

const int ledPin = 2;
const int motorPinA = 4;
const int motorPinB = 5;

int targetMotorSpeed = 0;
const unsigned int motorUpdateIntervalMs = 250;
long nextMotorUpdateAtMs = 0;

void setup() {
  Serial.begin(115200);

  pinMode(motorPinA, OUTPUT);
  pinMode(motorPinB, OUTPUT);

  setMotorSpeed(1024);
  delay(25);
  setMotorSpeed(0);

  settings = new YoYoSettings(512); //Settings must be created here in Setup() as contains call to EEPROM.begin() which will otherwise fail
  wifiManager.init(settings, onceConnected, NULL, NULL, false, 80, ledPin, HIGH);

  const char *macAddress = (*settings)["pair"];
  if(macAddress) setPair(macAddress);

  wifiManager.begin("Home Network Study", "blinkblink");
}

void onceConnected() {
  for(int i=0; i<3; ++i) {
    wifiManager.setWifiLED(HIGH);
    delay(150);
    wifiManager.setWifiLED(LOW);
    delay(150);
  }
  wifiManager.end();
  
  if (approx.init()) {
    approx.setProximateDeviceHandler(onProximateDevice, APPROXIMATE_INTIMATE_RSSI, /*lastSeenTimeoutMs*/ 3000);
    approx.setActiveDeviceHandler(onActiveDevice, /*inclusive*/ false);
    approx.begin();
  }
}

void loop() {
  wifiManager.loop();
  approx.loop();

  updateMotorSpeed();
}

void onProximateDevice(Device *device, Approximate::DeviceEvent event) {
  switch (event) {
    case Approximate::ARRIVE:
      wifiManager.setWifiLED(HIGH);
      char macAdddress[18];
      device -> getMacAddressAs_c_str(macAdddress);
      (*settings)["pair"] = macAdddress;
      settings->save();
      setPair(macAdddress);
      break;
    case Approximate::DEPART:
      wifiManager.setWifiLED(LOW);
      break;
  }
}

void setPair(const char *macAddress) {
  Serial.printf("Paired with: %s\n", macAddress);
  approx.setActiveDeviceFilter(macAddress);
}

void onActiveDevice(Device *device, Approximate::DeviceEvent event) {
  int payloadSizeByte = device -> getPayloadSizeBytes();
  if(device -> isDownloading()) payloadSizeByte *= -1;
  
  setTargetMotorSpeed(payloadSizeByte);
}

void updateMotorSpeed() {
  if(millis() > nextMotorUpdateAtMs) {
    setMotorSpeed(targetMotorSpeed);

    targetMotorSpeed = 0;
    nextMotorUpdateAtMs = millis() + motorUpdateIntervalMs;
  }
}

void setTargetMotorSpeed(int v) {
  targetMotorSpeed = constrain(v, -1024, 1024);
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
