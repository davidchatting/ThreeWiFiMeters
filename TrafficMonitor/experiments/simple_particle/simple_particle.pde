PVector p = new PVector();
PVector t = new PVector();
int sourceRadius = 400;

float mass = 1.0f;
PVector velocity;

//int step = 3;

void setup() {
  size(320, 480, P3D);
  background(0);
}

void draw() {
}

void mouseClicked() {
  boolean incoming = random(0,100) > 25;
  drawParticle(mouseX, mouseY, (int)random(100,200), incoming);
}

void drawParticle(int cx, int cy, int size, boolean incoming) {
  background(0);

  float a = random(0, TWO_PI);
  if(incoming) {
    p.x = (sourceRadius * cos(a)) + cx;
    p.y = (sourceRadius * sin(a)) + cy;

    t.x = cx;
    t.y = cy;
  }
  else {
    t.x = (sourceRadius * cos(a)) + cx;
    t.y = (sourceRadius * sin(a)) + cy;

    p.x = cx;
    p.y = cy;
  }

  float ta = a + random(-HALF_PI, HALF_PI);
  float da = random(20, 100);
  float dtx = t.x + (da * cos(ta));
  float dty = t.y + (da * sin(ta));

  float pa = atan2((dty-p.y), (dtx-p.x));
  velocity = PVector.fromAngle(pa);

  noFill();

  beginShape();

  float dSq = Float.MAX_VALUE;
  for (int n = 0; dSq > 10.0f && (n < sourceRadius * 100); n++) {
    PVector g = new PVector(t.x - p.x, t.y - p.y, 0.0);

    dSq = g.magSq();

    if (dSq > 10.0f) {
      float ga = 2.0f / dSq;

      g.normalize();
      g.mult(ga);
      stroke(255, size);
      
      velocity.mult(0.998f);
      velocity.add(g);

      p.add(velocity);

      vertex(p.x, p.y);
    }
  }
  endShape();
}
