/*
    Three WiFi Meters - Traffic Monitor
    -
    David Chatting - github.com/davidchatting/ThreeWiFiMeters
    MIT License - Copyright (c) March 2021
    Example documented here > https://github.com/davidchatting/ThreeWiFiMeters/tree/master#traffic-monitor
*/

class Observations {
  private int durationMs = 0; 
  private ArrayList<Observation> traffic = new ArrayList<Observation>();
  
  Observations(int durationMs) {
    this.durationMs = durationMs;
  }
  
  void add(int lengthInBytes, long timeMs){
    if(lengthInBytes > 0) {
      traffic.add(new Observation(lengthInBytes, timeMs));
    }
  }
  
  void update() {
    try {
      for (int i = 0; i < traffic.size();) {
        Observation o = traffic.get(i);
        if((millis() - durationMs) > o.timeMs) {
          traffic.remove(i);
        }
        else i++;
      }
    }
    catch(Exception e) {}
  }
  
  int count(long startMs, long endMs) {
    int total = 0;
    
    try {
      for (int i = 0; i < traffic.size(); i++) {
        Observation o = traffic.get(i);
        if(o.timeMs < endMs) {
          if(o.timeMs > startMs) {
            total += o.payloadLengthInBytes;
          }
        }
      }
    }
    catch(Exception e) {}
    
    return(total);
  }
}
