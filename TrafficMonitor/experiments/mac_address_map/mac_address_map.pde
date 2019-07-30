String macAddress[] = {"b0:72:bf:25:c3:41", "68:27:37:06:42:5c", "00:13:ef:c1:02:3b", "58:ef:68:b7:2b:dc", "b8:27:eb:97:36:f3", "20:df:b9:b1:c1:cc", "54:60:09:e4:b0:bc", "a4:77:33:1b:c1:bc", "f0:18:98:6b:d3:df", "b8:27:eb:c7:f6:a9", "a4:38:cc:dd:54:e5", "a0:d7:95:39:b4:44", "18:74:2e:52:23:80"};

void setup() {
  size(320, 480);
  stroke(255);
  noFill();
}

void draw() {
  background(0);
  circle(width/2, height/2, width);

  for (int n=0; n < macAddress.length; ++n) {
    drawMacAddress(macAddress[n]);
  }
}

void drawMacAddress(String macAddress) {
  //First 3 bytes are the manufacturer (OUI)
  String hex[] = macAddress.split(":");

  int oui = unhex(hex[0] + hex[1] + hex[2]);
  int device = unhex(hex[3] + hex[4] + hex[5]);

  println(macAddress);
  println(hex(oui) + "  " + hex(device));

  float a = ((oui & 0x00FFFF00) >> 8) / (float) 0xFFFF;
  float d = ((oui & 0x000000FF) >> 0) / (float) 0x00FF;

  int radius = (int)((width/2) * 0.95f);
  int dradius = (int)((width/2) * 0.05f);
  //but runs of devices might be quite close... so small differerence need to be visible...
  float da = (device % 0xFF) / (float)0xFF;

  int x = (int) (d * radius * cos(a * TWO_PI)) + (width/2) + (int)(dradius * cos(da * TWO_PI));
  int y = (int) (d * radius * sin(a * TWO_PI)) + (height/2) + (int)(dradius * sin(da * TWO_PI));

  circle(x, y, 3);
}
