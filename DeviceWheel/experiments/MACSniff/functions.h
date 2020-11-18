// This-->tab == "functions.h"

// Expose Espressif SDK functionality
extern "C" {
#include "user_interface.h"
  typedef void (*freedom_outside_cb_t)(uint8 status);
  int  wifi_register_send_pkt_freedom_cb(freedom_outside_cb_t cb);
  void wifi_unregister_send_pkt_freedom_cb(void);
  int  wifi_send_pkt_freedom(uint8 *buf, int len, bool sys_seq);
}

#include <ESP8266WiFi.h>
#include "./structures.h"

#define MAX_APS_TRACKED 100
#define MAX_CLIENTS_TRACKED 200

int aps_known_count = 0;                                  // Number of known APs
int nothing_new = 0;
int clients_known_count = 0;                              // Number of known CLIENTs

void promisc_cb(uint8_t *buf, uint16_t len)
{
  // Position 12 in the array is where the packet type number is located
  // For info on the different packet type numbers check:
  // https://stackoverflow.com/questions/12407145/interpreting-frame-control-bytes-in-802-11-wireshark-trace
  // https://supportforums.cisco.com/document/52391/80211-frames-starter-guide-learn-wireless-sniffer-traces
  // https://ilovewifi.blogspot.mx/2012/07/80211-frame-types.html
  if((buf[12]==0x88)||(buf[12]==0x40)||(buf[12]==0x94)||(buf[12]==0xa4)||(buf[12]==0xb4)||(buf[12]==0x08))
  {
    //Serial.printf("%02x\n",buf[12]);
    if(buf[12]==0x40) Serial.printf("Disconnected");
    else if(buf[12]==0x08) Serial.printf("Data");
    else if(buf[12]==0x88) Serial.printf("QOS");
    else Serial.printf("%02x\t",buf[12]);
    Serial.printf("\t");
    
    // Origin MAC address starts at byte 22
    // Print MAC address
    for(int i=0;i<5;i++) {
      Serial.printf("%02x:",buf[22+i]);
    }
    Serial.printf("%02x\t",buf[22+5]);
    // Signal strength is in byte 0
    Serial.printf("%i\n",int8_t(buf[0]));

    // Enable this lines if you want to scan for a specific MAC address
    // Specify desired MAC address on line 10 of structures.h
    /*int same = 1;
    for(int i=0;i<6;i++)
    {
      if(buf[22+i]!=desired[i])
      {
        same=0;
        break;
      }
    }
    if(same)
    {

    }
    //different device
    else
    {

    }*/
  }
  //Different packet type numbers
  else
  {

  }
}
