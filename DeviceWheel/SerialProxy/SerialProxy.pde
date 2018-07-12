import processing.serial.*;

Serial nodeMCU;
Serial arduino;

void setup() 
{
  size(200, 200);
  println(Serial.list());
  
  nodeMCU = new Serial(this, "/dev/tty.wchusbserial1420", 115200);
  arduino = new Serial(this, "/dev/tty.usbserial-A700dX9l", 115200);
}

void draw()
{
  if ( nodeMCU.available() > 0) {
    String s = nodeMCU.readStringUntil('\n');
    if(s != null){
      char direction = s.charAt(0);
      if(direction == '>' || direction == '<'){
        arduino.write(s);
      }
      else{
        println(s);
      }
    }
  }
}