/* LED CONTROLLING WITH PYTHON
 * Written by Junicchi
 * https://github.com/Kebablord 
 *
 * It's a ESP management through Python example
 * It simply fetches the path from the request
 * Path is: https://example.com/this -> "/this"
 * You can command your esp through python with request paths
 * You can read the path with getPath() function
 */


#include "ESP_MICRO.h"

#define LED 16

void setup(){
  Serial.begin(115200);
  start("FAMILIA LUZ","a1s2d3f4"); // Wifi details connec toxnx
  pinMode(LED,OUTPUT);
}

void loop(){
  waitUntilNewReq();  //Waits until a new request from python come

  if (getPath()=="/OPEN_LED"){
    printf("Foi no ON");
    digitalWrite(LED,HIGH);
  }
  if (getPath()=="/CLOSE_LED"){
    digitalWrite(LED,LOW);
    printf("Foi no ON");
  }
}
