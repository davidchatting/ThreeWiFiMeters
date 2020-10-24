import processing.serial.*;
import java.util.Map;

int cx, cy;
int portalDiameter;
int devicesRingRadius;
int graphMinDiameter;
int graphMaxDiameter;
int graphAxisDiameter;

Serial sniffer;

class Device {
  String macAddress;
  int position;
  long lastActiveMs;
};

HashMap<String,Device> devices = new HashMap<String,Device>();

boolean positionAllocation[] = new boolean[60];
int uploadTraffic[] = new int[60];
int downloadTraffic[] = new int[60];

int uploadTotalBytes = 0;
int downloadTotalBytes = 0;

void setup() {
  frameRate(60);
  
  sniffer = new Serial(this, "/dev/tty.usbserial-1410", 9600);
  sniffer.bufferUntil('\n');
  
  size(320, 480, P2D);
  smooth(8);
  
  cx = int(width/2);
  cy = int(height-(width/2)) + 10;
  portalDiameter = min(width, height)-28;
  
  devicesRingRadius = (portalDiameter - 8)/2;
  
  graphMinDiameter = 32;
  graphMaxDiameter = portalDiameter - 32;
  
  graphAxisDiameter = graphMinDiameter + (graphMaxDiameter - graphMinDiameter)/2;
}

void draw() {
  background(0);
  
  noFill();
  stroke(20);
  circle(cx, cy, portalDiameter);
  circle(cx, cy, graphMaxDiameter);
  circle(cx, cy, graphAxisDiameter);
  circle(cx, cy, graphMinDiameter);
  
  stroke(200);
  int s = second();
  for(int t=0; t < 60; ++t) {
    
    int n = (s-t) >= 0 ?  (s-t) : 60+(s-t);
    int alpha = (int) map(n, 60, 0,  0, 255);
    drawSecond(t, plot(uploadTraffic[t]), plot(downloadTraffic[t]), alpha);
  }
  
  stroke(200);
  for (Map.Entry me : devices.entrySet()) {
    Device thisDevice = (Device) me.getValue();
    
    if(thisDevice.lastActiveMs > (millis() - 60000)) {
      float a = map(thisDevice.position, 0, 60, 0, TWO_PI);
      int x = cx + (int)(devicesRingRadius * sin(a));
      int y = cy + (int)(devicesRingRadius * cos(a));
      
      stroke(255);
      if(thisDevice.lastActiveMs > (millis() - (1000/frameRate))) {
        fill(255);
      }
      else noFill();
      circle(x, y, 8);
    }
  }
  
  if(frameCount % 60 == 0) tick();  //once a second
}

void drawSecond(int t, float up, float down, int alpha) {
  float m = map(t, 0, 60, 0, TWO_PI) - HALF_PI;
  float ma = m - (TWO_PI/60.0f)/2.0f;
  float mb = m + (TWO_PI/60.0f)/2.0f;
  
  up = up * (graphMaxDiameter - graphAxisDiameter);
  down = down * (graphAxisDiameter - graphMinDiameter);
  
  noStroke();
  fill(200, alpha);
  arc(cx, cy, graphAxisDiameter + up, graphAxisDiameter + up, ma, mb);
  fill(0);
  arc(cx, cy, graphAxisDiameter - down, graphAxisDiameter - down, ma, mb);
}

int allocatePosition(String macAddress){
  int position = 0;
  
  String bytes[] = macAddress.split(":");
  position = (int)map(unhex(bytes[5]), 0, 255, 0, 59);
  
  while(positionAllocation[position]) {
    position = (position + 1) % 60;
  }
  positionAllocation[position] = true;
  
  return(position);
}

void tick() {  
  uploadTraffic[second()] = uploadTotalBytes;
  downloadTraffic[second()] = downloadTotalBytes;
   
  uploadTotalBytes = 0;
  downloadTotalBytes = 0;
}

float plot(int v) {
  float result = 0.0f;
  
  if(v > 0) {
    result = min(1.0f, map(log(v), 0, 10, 0, 1));
  }
  
  return(result);
}

void serialEvent (Serial port) {
  String reading = port.readStringUntil('\n');

  if (reading != null && reading.startsWith("[aprx]")) {
    println(reading);
    
    String s[] = reading.split("\t");
    //[aprx]  54:60:09:E4:B0:BC  2324
    String macAddress = s[1].trim();
    
    Device thisDevice = devices.get(macAddress);
    if(thisDevice == null) {
      thisDevice = new Device();
      thisDevice.macAddress = macAddress;
      thisDevice.position = allocatePosition(macAddress);
      
      devices.put(macAddress, thisDevice);
    }
    thisDevice.lastActiveMs = millis();
    
    uploadTotalBytes += int(s[2].trim());
    downloadTotalBytes += int(s[3].trim());
  }
}
