
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

#if defined(ESP8266)
  const int ledPin = 2;
#elif defined(ESP32)
  const int ledPin = 14;
#endif

const int motorPinA = SDA;
const int motorPinB = SCL;
#if defined(ESP32)
  const int motorChannelA = 0;
  const int motorChannelB = 1;
#endif

int targetMotorSpeed = 0;
const unsigned int motorUpdateIntervalMs = 250;
long nextMotorUpdateAtMs = 0;

bool newPair = false;

void setup() {
  Serial.begin(115200);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  pinMode(motorPinA, OUTPUT);
  pinMode(motorPinB, OUTPUT);
  #if defined(ESP32)
    ledcSetup(motorChannelA, 1000, 8);
    ledcSetup(motorChannelB, 1000, 8);
    ledcAttachPin(motorPinA, motorChannelA);
    ledcAttachPin(motorPinB, motorChannelB);
  #endif

  setMotorSpeed(1024);
  delay(25);
  setMotorSpeed(0);

  settings = new YoYoSettings(512); //Settings must be created here in Setup() as contains call to EEPROM.begin() which will otherwise fail
  wifiManager.init(settings, onceConnected, NULL, NULL, false, 80, -1);

//  const char *macAddress = (*settings)["pair"];
//  if(macAddress) setPair(macAddress);

  //Attempt to connect to a WiFi network previously saved in the settings, 
  //if one can not be found start a captive portal called "YoYoMachines", 
  //with a password of "blinkblink" to configure a new one:
  wifiManager.begin("Home Network Study", "blinkblink");
}

void onceConnected() {
  wifiManager.end();
  
  if (approx.init("","")) {
    approx.setProximateDeviceHandler(onProximateDevice, APPROXIMATE_INTIMATE_RSSI, /*lastSeenTimeoutMs*/ 3000);
    approx.setActiveDeviceHandler(onActiveDevice, /*inclusive*/ false);
    approx.begin();
  }
}

void loop() {
  uint8_t wifiStatus = wifiManager.loop();
  approx.loop();

  if(approx.isRunning()) {
    if(!newPair) digitalWrite(ledPin, HIGH);
    else {
      digitalWrite(ledPin, LOW);
      delay(200);
      digitalWrite(ledPin, HIGH);
      newPair = false;
    }
  }
  else {
    switch(wifiManager.currentMode) {
      case YoYoWiFiManager::YY_MODE_PEER_CLIENT:
        digitalWrite(ledPin, blink(1000));
        break;
      default:  //YY_MODE_PEER_SERVER
        digitalWrite(ledPin, blink(500));
        break;
    }
  }

  updateMotorSpeed();
}

bool blink(int periodMs) {
  return(((millis() / periodMs) % 2) == 0);
}

void onProximateDevice(Device *device, Approximate::DeviceEvent event) {
  switch (event) {
    case Approximate::ARRIVE:
      newPair = true;
      char macAdddress[18];
      device -> getMacAddressAs_c_str(macAdddress);
      (*settings)["pair"] = macAdddress;
      settings->save();
      setPair(macAdddress);
      break;
    case Approximate::DEPART:
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

  #if defined(ESP32)
    ledcWrite(motorChannelA, valueA);
    ledcWrite(motorChannelB, valueB);
  #else
    analogWrite(motorPinA, valueA);
    analogWrite(motorPinB, valueB);
  #endif
}
