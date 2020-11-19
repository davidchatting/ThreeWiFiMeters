import processing.serial.*;
import java.util.Map;

int cx, cy;
int consoleWidth, consoleHeight;
int portalDiameter;
int devicesRingRadius;
int graphMinDiameter;
int graphMaxDiameter;
int graphAxisDiameter;

Serial sniffer;

HashMap<Integer,String> ouiTable = new HashMap<Integer,String>();
HashMap<String,Device> devices = new HashMap<String,Device>();

boolean positionAllocation[] = new boolean[60];

Observations uploadTraffic = new Observations();
Observations downloadTraffic = new Observations();

long nowMs = 0;
int currentInterval = 0;
int frameRate = 60;
//int tickIntervalMs = 1000;

int cycles = 5;
int samplesPerCycle = 60;
int interval;

PFont font;
int textHeightPx = 10;

StringList console = new StringList();

void setup() {
  frameRate(frameRate);
  noCursor();
  
  size(320, 480, P2D);
  smooth(8);
  
  cx = int(width/2);
  cy = int(height-(width/2)) + 10;
  portalDiameter = min(width, height)-28;
  
  interval = ((portalDiameter/2)/(cycles-1))/2;
  
  devicesRingRadius = (portalDiameter - 8)/2;
  
  graphMinDiameter = 32;
  graphMaxDiameter = portalDiameter - 32;
  
  graphAxisDiameter = 64;  //graphMinDiameter + (graphMaxDiameter - graphMinDiameter)/2;
  
  consoleWidth = width;
  consoleHeight = cy - (portalDiameter/2);
  
  font = createFont("Helvetica", textHeightPx);
  textFont(font);
  
  loadOuiTable();
  
  try{
    sniffer = new Serial(this, getArduinoPort(), 115200);
    sniffer.bufferUntil('\n');
  }
  catch(Exception e) {}
}

void draw() {  
  background(0);
  
  drawConsole(0, 0, consoleWidth, consoleHeight);
  
  noFill();
  stroke(20, 255);
  circle(cx, cy, portalDiameter);
  
  //drawGraph(cx, cy);
  strokeWeight(3);
  drawSpiral(cx, cy, graphMaxDiameter);
  strokeWeight(2);
  drawDevices();
}

void drawConsole(int x, int y, int w, int h) {
  stroke(200, 255);
  fill(200, 255);
  String s ="";
  for(int n = 0; n < console.size(); ++n) {
    s += console.get(n);
  }
  
  text(s, x + 10, y);
}


void drawSpiral(int cx, int cy, int diameter) {
  int tickIntervalMs = 60000 / samplesPerCycle;
  int t = (int)(samplesPerCycle * (second()/60.0f));
  
  if(t != currentInterval) {
    currentInterval = t;
    nowMs += tickIntervalMs;
  }
  
  float r = 0;
  float step=(diameter/2.0f)/(samplesPerCycle * (cycles +1));
  
  float x, y;
  float da = (TWO_PI/samplesPerCycle);
  int alpha;
  
  int n = (samplesPerCycle * cycles);
  
  noFill();
  for (int i = 0 ; i <= n ; i++ ){
    int dtSec = -1 * (n-i);
    
    alpha = (i<samplesPerCycle/2)? 0 : 255;  //(int) map(i, 0, (samplesPerCycle * cycles), 0, 255);
    
    if(dtSec == 0) stroke(255, 0, 0, alpha);
    else stroke(255, alpha);
    
    float a = PI - (da*i);
    x = r * sin(a);
    y = r * cos(a);
    
    long startMs = nowMs + (dtSec * tickIntervalMs);
    long endMs = startMs + tickIntervalMs;
    
    int up = uploadTraffic.count(startMs, endMs);
    int down = downloadTraffic.count(startMs, endMs);
    
    drawTick(cx + x, cy + y, a, max(0.1f, normalise(up + down) * interval/2.0f));
    r += step;
  }
}

void drawTick(float cx, float cy, float a, float l) {
  float cxb, cyb;
  
  cxb = cx + (l * sin(a));
  cyb = cy + (l * cos(a));
  
  line(cx, cy, cxb, cyb);
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
  String manufacturer = ouiTable.get(getOUI(macAddress));
  
  if(true) {
  //if(macAddress.equals("A4:77:33:1B:C1:BC")){
  //if(manufacturer != null) {
    //println(uploadBytes + "  " + downloadBytes);
    
    long now =  millis();
    Device thisDevice = devices.get(macAddress);
    if(thisDevice == null) {
      byte mostSigByte = (byte) unhex(macAddress.split(":")[0]);
      
      addToConsole(macAddress + " (" + manufacturer + ")\n");
      
      thisDevice = new Device();
      thisDevice.macAddress = macAddress;
      thisDevice.position = allocatePosition(macAddress);
      
      devices.put(macAddress, thisDevice);
    }
    thisDevice.lastActiveMs = now;
    
    uploadTraffic.add(uploadBytes, now);
    downloadTraffic.add(downloadBytes, now);
  }
}

int getOUI(String macAddress) {
  int oui = 0;
  
  String bytes[] = macAddress.split(":");
  oui = (unhex(bytes[0]) << 16) + (unhex(bytes[1]) << 8) + unhex(bytes[2]);
  
  return(oui);
}

void loadOuiTable() {
  //http://linuxnet.ca/ieee/oui/nmap-mac-prefixes
  
  addToConsole("Loading OUI table...\t");
  String[] prefixes = loadStrings("nmap-mac-prefixes");
  for(int n=0; n < prefixes.length; ++n) {
    String[] p = prefixes[n].split("\t");
    ouiTable.put(unhex(p[0]), p[1]);
  }
  addToConsole("DONE\n");
}

String getArduinoPort() {
  String port = null;
  
  String serialList [] = Serial.list();
  for (int n=0; n < serialList.length && port==null; ++n) {
    if (looksLikeArduino(serialList[n])) {
      port = serialList[n];
    }
  }
  addToConsole("Arduino Port: " + port + "\n");
  
  return(port);
}

boolean looksLikeArduino(String s) {
  return(s.startsWith("/dev/tty.usb") || s.equals("/dev/cu.SLAB_USBtoUART") || s.startsWith("/dev/ttyUSB"));
}

void addToConsole(String line) {
  print(line);
  console.append(line);
}
