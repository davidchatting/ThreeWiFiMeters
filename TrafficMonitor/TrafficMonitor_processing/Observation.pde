/*
    Three WiFi Meters - Traffic Monitor
    -
    David Chatting - github.com/davidchatting/ThreeWiFiMeters
    MIT License - Copyright (c) March 2021
    Documented here > https://github.com/davidchatting/ThreeWiFiMeters/tree/master#traffic-monitor
*/

class Observation {
  int payloadLengthInBytes;
  long timeMs;
  
  Observation(int l, long t) {
    payloadLengthInBytes = l;
    timeMs = t;
  }
}
