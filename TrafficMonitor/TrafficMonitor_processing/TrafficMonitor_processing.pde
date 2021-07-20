/*
  Three WiFi Meters - Traffic Monitor
  -
   David Chatting - github.com/davidchatting/ThreeWiFiMeters
   MIT License - Copyright (c) March 2021
   Documented here > https://github.com/davidchatting/ThreeWiFiMeters#-traffic-monitor
 */

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
String serialPort = null;
int reconnectIntervalMs = 10000;
long reconnectDueAtMs = 0;

HashMap<Integer, String> ouiTable = new HashMap<Integer, String>();
HashMap<String, Device> devices = new HashMap<String, Device>();

boolean positionAllocation[] = new boolean[60];

long nowMs = 0;
int currentInterval = 0;
int frameRate = 12;

int requestObservationsIntervalMs = 500;
long requestObservationsDueAtMs = 0;

int cycles = 3 + 1;
int samplesPerCycle = 60;
float[] ticks = new float[(cycles - 1) * samplesPerCycle];
int interval;

Observations uploadTraffic = new Observations(cycles * 60 * 1000);
Observations downloadTraffic = new Observations(cycles * 60 * 1000);

int flashThresholdMs = (int) (1000 * 0.3f);

PFont font;
int textHeightPx = 10;
int consoleLineNumber = 1;

void setup() {
  frameRate(frameRate);
  noCursor();

  size(320, 480, JAVA2D);
  background(0);
  smooth(2);

  cx = int(width/2);
  cy = int(height-(width/2)) + 10;
  portalDiameter = min(width, height)-28;

  interval = ((portalDiameter/2)/(cycles-1))/2;

  devicesRingRadius = (portalDiameter - 8)/2;

  graphMinDiameter = 32;
  graphMaxDiameter = portalDiameter - 32;

  graphAxisDiameter = 64;

  consoleWidth = width;
  consoleHeight = cy - (portalDiameter/2);

  font = createFont("Courier", textHeightPx);
  textFont(font);

  loadOuiTable();
  connectSniffer();

  nowMs = (millis()/1000) * 1000;
}

void draw() {  
  background(0);

  updateTicks();

  try {
    drawConsole(0, 0, consoleWidth, consoleHeight);

    noFill();
    stroke(20, 255);
    circle(cx, cy, 8 );
    circle(cx, cy, portalDiameter);

    drawDevices(cx, cy);
    drawSpiral(cx, cy, graphMaxDiameter);
  }
  catch(Exception e) {
  }

  if (millis() > reconnectDueAtMs) connectSniffer();
  requestObservations();
}

void serialEvent(Serial port) {
  readObservations();
}

void connectSniffer() {
  try {
    serialPort = getArduinoPort();
    sniffer = new Serial(this, serialPort, 115200);
    sniffer.bufferUntil('\n');
  }
  catch(Exception e) {
  }

  delay(1000);
}

void requestObservations() {
  if (sniffer != null && millis() > requestObservationsDueAtMs) {
    sniffer.write('x');
    requestObservationsDueAtMs = millis() + requestObservationsIntervalMs;

    uploadTraffic.update();
    downloadTraffic.update();
  }
}

void readObservations() {
  if (sniffer != null) {
    while (sniffer.available() > 0) {
      String reading = sniffer.readStringUntil('\n');

      if (reading != null && reading.startsWith("[aprx]")) {
        
        String s[] = reading.split("\t");  //[aprx]  YY_IDLE_STATUS  54:60:09:E4:B0:BC  2324
        if (s.length == 5) {
          addObservation(s[2].trim(), int(s[3].trim()), int(s[4].trim()));
        }

        reconnectDueAtMs = millis() + reconnectIntervalMs;
      }
    }
  }
}

void drawConsole(int x, int y, int w, int h) {
  stroke(200, 255);
  fill(200, 255);
  
  resetConsoleLine();
  drawConsoleLine(x, y, w, h, ((millis() < reconnectDueAtMs)?"CONNECTED":"NOT CONNECTED") + "\t(" + ((serialPort!=null)?(serialPort):"NONE") + ")");
  drawConsoleLine(x, y, w, h, "-");

  for (Map.Entry me : devices.entrySet()) {
    Device thisDevice = (Device) me.getValue();

    if ((thisDevice.manufacturer == null || !thisDevice.manufacturer.equals("Espressif")) && thisDevice.lastActiveMs > (millis() - 60000)) {
      fill(200);
      if (thisDevice.lastActiveMs > (millis() - flashThresholdMs)) {
        fill(255);
      }
      drawConsoleLine(x, y, w, h, thisDevice.macAddress + ((thisDevice.manufacturer == null) ? "" : "\t" + thisDevice.manufacturer));
    }
  }
}

void drawConsoleLine(int x, int y, int w, int h, String s) {
  int maxConsoleLineNumber = (int)(h/(textHeightPx*1.2f));
  
  if(consoleLineNumber < maxConsoleLineNumber) {
    text(s, x + 10, y + ((textHeightPx + 2) * consoleLineNumber));
    consoleLineNumber++;
  }
}

void resetConsoleLine() {
  consoleLineNumber = 1;
}

void updateTicks() {
  int tickIntervalMs = 60000 / samplesPerCycle;
  int t = (int)(samplesPerCycle * (second()/60.0f));

  if (t != currentInterval) {
    for (int n = ticks.length-1; n > 0; --n) ticks[n] = ticks[n-1];

    int dtSec = -1;
    long startMs = nowMs + (dtSec * tickIntervalMs);
    long endMs = startMs + tickIntervalMs;

    int up = uploadTraffic.count(startMs, endMs);
    int down = downloadTraffic.count(startMs, endMs);
    ticks[0] = normalise(up + down) * interval/2.0f;

    currentInterval = t;
    nowMs += tickIntervalMs;
  }
}

void drawSpiral(int cx, int cy, int diameter) {
  noFill();

  float x, y;
  float da = (TWO_PI/samplesPerCycle);

  float r = 0;
  float step=(diameter/2.0f)/(samplesPerCycle * (cycles +1));

  for (int n = 0; n <= (samplesPerCycle * cycles); n++ ) {
    int i = (samplesPerCycle * cycles) - n;

    r = i * step;

    strokeWeight(i/samplesPerCycle);

    float a = PI - (da*i);
    x = r * sin(a);
    y = r * cos(a);

    color c = color(0); 
    float v = ticks[n];
    if (n == 0) c = color(255, 0, 0);
    else {
      c = color((v == 0.0f)? 20 : 255);
    }
    drawTick(cx + x, cy + y, a, v, c);
  }
}

void drawTick(float cx, float cy, float a, float l, color c) {
  float cxb, cyb;

  if (l == 0) l = 1.0f;//0.1f;

  cxb = cx + (l * sin(a));
  cyb = cy + (l * cos(a));

  stroke(c);
  line(cx, cy, cxb, cyb);
}

void drawDevices(int cx, int cy) {
  strokeWeight(1);

  for (Map.Entry me : devices.entrySet()) {
    Device thisDevice = (Device) me.getValue();

    if (thisDevice.manufacturer != null && thisDevice.lastActiveMs > (millis() - 60000)) {
      float a = map(thisDevice.position, 0, 60, 0, TWO_PI);
      int x = cx + (int)(devicesRingRadius * sin(a));
      int y = cy + (int)(devicesRingRadius * cos(a));

      stroke(255);
      if (thisDevice.lastActiveMs > (millis() - flashThresholdMs)) {
        fill(255);
      } else noFill();
      circle(x, y, 8);
    }
  }
}

int allocatePosition(String macAddress) {
  int position = 0;

  String bytes[] = macAddress.split(":");
  position = (int)map(unhex(bytes[5]), 0, 255, 0, 59);

  while (positionAllocation[position]) {
    position = (position + 1) % 60;
  }
  positionAllocation[position] = true;

  return(position);
}

float normalise(int v) {
  float result = 0.0f;

  if (v > 0) {
    //approximation of the sigmoid function:
    result = map(v, 0, 2048, -6.0f, 6.0f);
    result = map(result / (1.0f + abs(result)), -1.0f, 1.0f, 0.0f, 1.0f);
  }

  return(result);
}

void addObservation(String macAddress, int uploadBytes, int downloadBytes) {
  if(!acceptPacket(macAddress)) return;
  
  long now =  millis();
  Device thisDevice = devices.get(macAddress);
  if (thisDevice == null) {
    thisDevice = new Device();
    thisDevice.macAddress = macAddress;
    thisDevice.manufacturer = ouiTable.get(getOUI(macAddress));
    
    //Ignore devices without a known manufacturer and other ESP devices
    thisDevice.position = allocatePosition(macAddress);
    devices.put(macAddress, thisDevice);
  }
  thisDevice.lastActiveMs = now;

  uploadTraffic.add(uploadBytes, now);
  downloadTraffic.add(downloadBytes, now);
}

boolean acceptPacket(String macAddress) {
  boolean result = true;
  
  result = result && !macAddress.endsWith("00:00:00");         //group address
  result = result && !macAddress.equals("FF:FF:FF:FF:FF:FF");  //broadcast address
  result = result && !macAddress.startsWith("01:00:5E");       //IPv4 multicast address
  result = result && !macAddress.startsWith("33:33");          //IPv6 multicast address
  result = result && !macAddress.startsWith("01:80:C2");       //Bridge address
  
  return(result);
}

int getOUI(String macAddress) {
  int oui = 0;

  String bytes[] = macAddress.split(":");
  oui = (unhex(bytes[0]) << 16) + (unhex(bytes[1]) << 8) + unhex(bytes[2]);

  return(oui);
}

void loadOuiTable() {
  //http://linuxnet.ca/ieee/oui/nmap-mac-prefixes

  String[] prefixes = loadStrings("nmap-mac-prefixes");
  for (int n=0; n < prefixes.length; ++n) {
    if(!prefixes[n].startsWith("#")) {
      String[] p = prefixes[n].split("\t");
      ouiTable.put(unhex(p[0]), p[1]);
    }
  }
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
  return(s.equals("/dev/serial0") || s.startsWith("/dev/tty.usb") || s.equals("/dev/cu.SLAB_USBtoUART") || s.startsWith("/dev/ttyUSB"));
}
