import processing.serial.*;
import java.util.Map;

int cx, cy;
int portalDiameter;
int devicesRingRadius;
int graphMinDiameter;
int graphMaxDiameter;
int graphAxisDiameter;

Serial sniffer;

HashMap<String,Device> devices = new HashMap<String,Device>();

boolean positionAllocation[] = new boolean[60];

Observations uploadTraffic = new Observations();
Observations downloadTraffic = new Observations();

long nowMs = 0;
int currentInterval = 0;
int frameRate = 60;
int tickIntervalMs = 1000;

void setup() {
  frameRate(frameRate);
  
  sniffer = new Serial(this, getArduinoPort(), 115200);
  sniffer.bufferUntil('\n');
  
  size(320, 480, P2D);
  smooth(8);
  
  cx = int(width/2);
  cy = int(height-(width/2)) + 10;
  portalDiameter = min(width, height)-28;
  
  devicesRingRadius = (portalDiameter - 8)/2;
  
  graphMinDiameter = 32;
  graphMaxDiameter = portalDiameter - 32;
  
  graphAxisDiameter = 64;  //graphMinDiameter + (graphMaxDiameter - graphMinDiameter)/2;
}

void draw() {
  int samplesPerMinute = 60000 / tickIntervalMs;
  int t = (int)(samplesPerMinute * (second()/60.0f));
  
  if(t != currentInterval) {
    currentInterval = t;
    nowMs += tickIntervalMs;
  }
  
  background(0);
  
  noFill();
  stroke(20);
  circle(cx, cy, portalDiameter);
  circle(cx, cy, graphMaxDiameter);
  circle(cx, cy, graphAxisDiameter);
  circle(cx, cy, graphMinDiameter);
  
  stroke(200);
  
  for(int n=0; n < samplesPerMinute; ++n) {
    int dt = (t-n) >= 0 ?  (t-n) : samplesPerMinute+(t-n);
    
    int alpha = (int) map(dt, samplesPerMinute, 0, 25, 255);
    
    long startMs = nowMs - (dt * tickIntervalMs);
    long endMs = startMs + tickIntervalMs;
    
    int up = uploadTraffic.count(startMs, endMs);
    int down = downloadTraffic.count(startMs, endMs);
    
    drawGraph(normalise(up), normalise(down), n, samplesPerMinute, alpha);
  }
  
  drawDevices();
}

void drawGraph(float up, float down, int t, int samplesPerMinute, int alpha) {
  float ma = map(t, 0, samplesPerMinute, 0, TWO_PI) - HALF_PI;
  float mb = ma + (TWO_PI/(float)samplesPerMinute);
  
  
  up = round(up * (graphMaxDiameter - graphAxisDiameter)/2);
  down = round(down * (graphMaxDiameter - graphAxisDiameter)/2);
  
  fill(200, alpha);
  noStroke();
  //stroke(200);
  arc(cx, cy, graphAxisDiameter + up + down, graphAxisDiameter + up + down, ma, mb);
  fill(0);
  //stroke(200, alpha);
  arc(cx, cy, graphAxisDiameter, graphAxisDiameter, ma, mb);
}

void drawDevices() {
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

float normalise(int v) {
  float result = 0.0f;
  
  if(v > 0) {
    //result = min(1.0f, map(log10(v), 0, 6, 0, 1));
    result = min(1.0f, map(v, 0, 262144, 0, 1));
  }
  
  return(result);
}

float log10 (float x) {
  return (log(x) / log(10));
}

void serialEvent (Serial port) {
  String reading = port.readStringUntil('\n');

  if (reading != null && reading.startsWith("[aprx]")) {
    String s[] = reading.split("\t");  //[aprx]  54:60:09:E4:B0:BC  2324    
    addObservation(s[1].trim(), int(s[2].trim()), int(s[3].trim()));
  }
}

void addObservation(String macAddress, int uploadBytes, int downloadBytes) {
  if(macAddress == "FF:FF:FF:FF:FF:FF") return;  //broadcast address
  
  long now =  millis();
  Device thisDevice = devices.get(macAddress);
  if(thisDevice == null) {
    thisDevice = new Device();
    thisDevice.macAddress = macAddress;
    thisDevice.position = allocatePosition(macAddress);
    
    devices.put(macAddress, thisDevice);
  }
  thisDevice.lastActiveMs = now;
  
  uploadTraffic.add(uploadBytes, now);
  downloadTraffic.add(downloadBytes, now);
}

String getArduinoPort() {
  String port = null;
  
  String serialList [] = Serial.list();
  for (int n=0; n < serialList.length && port==null; ++n) {
    if (looksLikeArduino(serialList[n])) {
      port = serialList[n];
    }
  }
  
  return(port);
}

boolean looksLikeArduino(String s) {
  return(s.startsWith("/dev/tty.usb"));
}
