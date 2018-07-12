#include "AccelStepper.h"
#define HALFSTEP 8

// Motor pin definitions
#define motorPin1  8  //D1     // IN1 on the ULN2003 driver 1
#define motorPin2  9  //D2     // IN2 on the ULN2003 driver 1
#define motorPin3  10 //D3     // IN3 on the ULN2003 driver 1
#define motorPin4  11 //D4     // IN4 on the ULN2003 driver 1

// Initialize with pin sequence IN1-IN3-IN2-IN4 for using the AccelStepper with 28BYJ-48
AccelStepper stepper(HALFSTEP, motorPin1, motorPin3, motorPin2, motorPin4);

void setup() {
  Serial.begin(115200);
  
  stepper.setMaxSpeed(1000.0);
  stepper.setAcceleration(1000.0);
  stepper.setSpeed(500);
}

void loop() {
  /*
  //Change direction when the stepper reaches the target position
  if (stepper1.distanceToGo() == 0) {
    stepper1.moveTo(-stepper1.currentPosition());
  }
  */

  stepper.run();
}

void serialEvent() {
  while (Serial.available() > 0) {
    char c = (char)Serial.read();
    int packetLength = parsePacketLength();

    switch(c){
      case '>':
        stepper.move(packetLength);
        break;
      case '<':
        stepper.move(-1*packetLength);
        break;
      default:
        break;
    }
  }
}

int parsePacketLength(){
  int packetLength=0;

  boolean eolFound = false;
  String number="";
  while (!eolFound) { // && Serial.available() > 0
    int b = Serial.read();
    if(b != -1){ 
      if((char)b != '\n'){
        number+=(char)b;
      }
      else {
        eolFound = true;
        packetLength = number.toInt();
      }
    }
  }
  
  return(packetLength);
}

