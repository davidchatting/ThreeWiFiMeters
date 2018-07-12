  import processing.serial.*;

  Serial myPort;        // The serial port
  int xPos = 1;         // horizontal position of the graph
  float inByte = 0;
  
  int buffer[];
  int lastReadingAtSec=second();
  int panelWidth=150;
  int maxValue;
  
  int whiteValue = 200;
  int blackValue = 50;

  void setup () {
    // set the window size:
    size(600, 600);
    frameRate(4);

    println(Serial.list());
    myPort = new Serial(this, "/dev/cu.wchusbserial1410", 9600);
    myPort.bufferUntil('\n');

    background(0);
    
    buffer = new int[60];
    
    maxValue = width/3;
  }

  void draw () {
    background(0);
    
    /*
    //stroke(255, 255, 255);
    noStroke();
    for(int n=0;n<buffer.length;++n){
      //point(width/2-n,height - buffer[n]);
      //if(n!=0) line(width/2-n, height - buffer[n-1], width/2-n-1, height - buffer[n]);
      //rect(width/2-(n*3),height,width/2-((n-1)*3),height - buffer[n]);
      int t=lastReadingAtSec-n;
      t=t<0?60+t:t;
      t=(int)map(t,0,60,255,20);
      fill(t, t, t);
      rect((n*5),height - buffer[n],5,buffer[n]);
    }
    */
    
    noFill();
    float da = TWO_PI/buffer.length;
    int n = lastReadingAtSec + 1;  //draw the clock oldest values first
    boolean finished = false;
    do {
      if(n == buffer.length) n = 0;
       
      float a = (n*-TWO_PI/buffer.length)+(da/2);  //0 is at 12 o'clock
      float l = (panelWidth/2)+map(buffer[n], 0, 100000, 0, maxValue);
      l=min(l,maxValue);
      
      //if(v!=0) point(100+(v*sin(a+PI)),100+(v*cos(a+PI)));
      
      int t=lastReadingAtSec-n;
      t=t<0?60+t:t;
      t=(int)map(t,0,60,whiteValue,blackValue);
      stroke(t, t, t);
      arc(width/2, height/2, l*2, l*2, -a-HALF_PI, -a-HALF_PI+da, PIE);
      
      if(n==lastReadingAtSec) finished = true;
      else ++n;
    } while(!finished);
    
    stroke(whiteValue);
    //noStroke();
    fill(0);
    ellipse(width/2, height/2, panelWidth, panelWidth);
  }

  void serialEvent (Serial myPort) {
    // get the ASCII string:
    String inString = myPort.readStringUntil('\n');

    if (inString != null) {
      // trim off any whitespace:
      inString = trim(inString);
      // convert to an int and map to the screen height:
      inByte = float(inString);
      println(inByte);
      
      lastReadingAtSec=second();
      buffer[lastReadingAtSec]=(int)inByte;
    }
  }