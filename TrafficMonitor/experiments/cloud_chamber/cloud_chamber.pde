
//
// David Chatting July 2019
// ---
// Based on metropop by Tom Carden, May 2004, revised May 2005.
// a simple particle system with naive gravitational attraction
//

int NUM_PARTICLES  = 1;  //10000;
int NUM_ATTRACTORS = 1;

Particle[] particle;
Attractor[] attractor;

void setup() {
  
  size(320,480,P3D);
  frameRate(90);

  attractor = new Attractor[NUM_ATTRACTORS];
  particle = new Particle[NUM_PARTICLES];
  
  scatter();
  
  // a favourite... (comment these out if you change NUM_ATTRACTORS)
  //attractor[0] = new Attractor(199.51851,109.791565);
  //attractor[1] = new Attractor(142.45416,273.7996);
  //attractor[2] = new Attractor(81.76278,28.523111);
  //attractor[3] = new Attractor(167.28207,196.15504);
  //attractor[4] = new Attractor(517.4808,312.41132);
  //attractor[5] = new Attractor(564.9883,7.6203823);

}

void draw() {
  // move and draw particles
  stroke(255,150); // use lower alpha for finer detail
  
  //for (int i = 0; i < attractor.length; i++) {
  //  rect(attractor[i].x, attractor[i].y, 10, 10);
  //}
  
  noFill();
  beginShape();
  for (int i = 0; i < particle.length; i++) {
    for (int n = 0; n < 1000; n++) {
      particle[i].step();
      vertex(particle[i].x,particle[i].y);
    }
  }
  endShape();
  
  // reset on mouse click
  if (mousePressed) {
    //saveFrame("metropop-######.png");
    scatter();
  }
}

void scatter() {

  // clear the preview
  background(0);

  int cx = int(width/2);
  int cy = int(height-(width/2)) + 10; //put it at the bottom of the screen
  int diameter = int(width/2) - 10;

  // randomise attractors
  for (int i = 0; i < attractor.length; i++) {
    float a = random(TWO_PI);
    float d = random(0,diameter);
    float x = cx + (d * sin(a));
    float y = cy + (d * cos(a));
    
    attractor[i] = new Attractor(x,y);
    println("attractor["+i+"] = new Attractor("+attractor[i].x+","+attractor[i].y+");"); // so you *can* get your favourite one back, if you want!
  }
  println();
  
  // randomise particles
  for (int i = 0; i < particle.length; i++) {
    particle[i] = new Particle(width/2, height/2);
  }
  
}
