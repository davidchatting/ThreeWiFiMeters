
// a point in space with a velocity
// moves according to acceleration and damping parameters
// in this case, it moves very fast so the process is basically "scattering"

// changing these parameters can give very different results
float damp = 0.995f;  //0.00002; // remember a very small amount of the last direction
float accel = 1.0f; //4000.0; // move very quickly

class Particle {
  // location and velocity
  float x,y,vx,vy;
  
  Particle(int targetX, int targetY) {
    init(targetX, targetY);
  }
  
  void init(int targetX, int targetY) {
    // initialise with random velocity:
    float a = random(TWO_PI);
    float dx = 1000 * sin(a);
    float dy = 1000 * cos(a);
    
    x = (width/2) + dx;
    y = (height/2) + dy;
    
    // initialise with random velocity:
    //vx = random(-accel/2,accel/2);
    //vy = random(-accel/2,accel/2);
    
    //Aim towards the centre of the screen:
    vx = -dx/targetX;
    vy = -dy/targetY;
  }
  
  
  void step() {
    // move towards every attractor 
    // at a speed inversely proportional to distance squared
    // (much slower when further away, very fast when close)
    
    for (int i = 0; i < attractor.length; i++) {
      
      // calculate the square of the distance 
      // from this particle to the current attractor
      float d2 = sq(attractor[i].x-x) + sq(attractor[i].y-y);

      if (d2 > 5) { // make sure we don't divide by zero
        // accelerate towards each attractor
        vx += accel * (attractor[i].x-x) / d2;
        vy += accel * (attractor[i].y-y) / d2;
      }
      else {
        vx = 0;
        vy = 0;
      }
      
    }
    
    // move by the velocity
    x += vx;
    y += vy;
    
    // scale the velocity back for the next frame
    vx *= damp;
    vy *= damp;
    
  }
  
  boolean reached(Attractor a){
    boolean result = false;
    
    result = sqrt(sq(a.x-x) + sq(a.y-y)) < 10.0f;
    
    return(result);
  }
}
