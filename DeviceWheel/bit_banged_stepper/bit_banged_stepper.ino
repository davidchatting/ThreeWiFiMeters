#define pin1  8//these are the Arduino pins that we use to activate coils 1-4 of the stepper motor
#define pin2  9
#define pin3  10
#define pin4  11

// Stepper
#define delaytime 3

void setup() {
  // initialize the 8 pin as an output:
  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
  pinMode(pin3, OUTPUT);
  pinMode(pin4, OUTPUT);
  Serial.begin(9600);

  while (true) {
    backward();
  }
}

void loop() {
}

//these functions set the pin settings for each of the four steps per rotation of the motor (keep in mind that the motor in the kit is geared down,
//i.e. there are many steps necessary per rotation

void setCoils(byte b){
  digitalWrite(pin1, bitRead(b,0));//turn on coil 1
  digitalWrite(pin2, bitRead(b,1));
  digitalWrite(pin3, bitRead(b,2));
  digitalWrite(pin4, bitRead(b,3));
}

//these functions run the above configurations in forward and reverse order
//the direction of a stepper motor depends on the order in which the coils are turned on.
void forward() { //one tooth forward
  byte b=1;

  for(int n=0;n<4;++n){
    setCoils(b);
    delay(delaytime);
    b = b << 1;
  }
}

void backward() { //one tooth backward
  byte b=8;

  for(int n=0;n<4;++n){
    setCoils(b);
    delay(delaytime);
    b = b >> 1;
  }
}

void step_OFF() {
  setCoils(0);
}
