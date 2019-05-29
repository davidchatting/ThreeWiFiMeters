const int motorPinA = 4;
const int motorPinB = 5;

const int minSpeed = 250;

void setup() {
  // put your setup code here, to run once:
  pinMode(motorPinA, OUTPUT);
  digitalWrite(motorPinA, LOW);
  pinMode(motorPinB, OUTPUT);
  digitalWrite(motorPinB, LOW);

  delay(50);
}

void loop() {
    setMotorSpeed(800);
    delay(700);

    setMotorSpeed(0);
    delay(1000);

    setMotorSpeed(-800);
    delay(1000);

    setMotorSpeed(0);
    delay(1000);
}

void setMotorSpeed(int v) {
  float valueA = 0;
  float valueB = 0;
  
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
  
  analogWrite(motorPinA, valueA);
  analogWrite(motorPinB, valueB);
}
