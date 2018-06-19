#include <AccelStepper.h>
#define HALFSTEP 8

// Motor pin definitions
#define motorPin1  D1     // IN1 on the ULN2003 driver 1
#define motorPin2  D2     // IN2 on the ULN2003 driver 1
#define motorPin3  D3     // IN3 on the ULN2003 driver 1
#define motorPin4  D4     // IN4 on the ULN2003 driver 1

// Initialize with pin sequence IN1-IN3-IN2-IN4 for using the AccelStepper with 28BYJ-48
AccelStepper stepper1(HALFSTEP, motorPin1, motorPin3, motorPin2, motorPin4);

void setup() {
  stepper1.setMaxSpeed(1000.0);
  stepper1.setAcceleration(100.0);
  stepper1.setSpeed(200);
  stepper1.moveTo(20000);

}//--(end setup )---

void loop() {

  //Change direction when the stepper reaches the target position
  if (stepper1.distanceToGo() == 0) {
    stepper1.moveTo(-stepper1.currentPosition());
  }
  stepper1.run();
}
