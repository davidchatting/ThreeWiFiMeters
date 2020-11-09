class Observation {
  int payloadLengthInBytes;
  long timeMs;
  
  Observation(int l, long t) {
    payloadLengthInBytes = l;
    timeMs = t;
  }
}
