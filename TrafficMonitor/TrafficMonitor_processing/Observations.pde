class Observations {
  ArrayList<Observation> traffic = new ArrayList<Observation>();
  
  void add(int lengthInBytes, long timeMs){
    if(lengthInBytes > 0) {
      traffic.add(new Observation(lengthInBytes, timeMs));
    }
  }
  
  int count(long startMs, long endMs) {
    int total = 0;
    
    for (int i = 0; i < traffic.size(); i++) {
      Observation o = traffic.get(i);
      if(o.timeMs < endMs) {
        if(o.timeMs > startMs) {
          total += o.payloadLengthInBytes;
        }
      }
    }
    
    return(total);
  }
}
