#include "ESP_MICRO.h"

#define LED 16

void setup()
{
  Serial.begin(115200);
  start("FAMILIA LUZ", "a1s2d3f4"); // Wifi details connec toxnx
  pinMode(LED, OUTPUT);
  //Define os pinos de controle do motor como saida
  //Motor 1
  pinMode(5, OUTPUT); // saída A-
  pinMode(0, OUTPUT); // saída A+
  //Motor 2
  pinMode(4, OUTPUT); // saída B-
  pinMode(2, OUTPUT); // saída B+
}

void loop()
{
  waitUntilNewReq(); //Waits until a new request from python come

  if (getPath() == "/front_AB")
  {
    printf("ON A");
    analogWrite(5, 1024);
    digitalWrite(0, LOW);
    printf("ON B");
    analogWrite(4, 1024);
    digitalWrite(2, HIGH);
  }
  if (getPath() == "/front_B")
  {
    printf("ON B");
    analogWrite(4, 1024);
    digitalWrite(2, HIGH);
  }
  
  if (getPath() == "/front_A")
  {
    printf("ON A");
    analogWrite(5, 1024);
    digitalWrite(0, LOW);
  }
  if (getPath() == "/back_AB")
  {
    printf("BACK A_B");
    // Aciona motor A
    analogWrite(5, 1024); 
    digitalWrite(0, HIGH); 
    //Aciona motor B
    analogWrite(4, 1024); 
    digitalWrite(2, LOW); 
  }

  if (getPath() == "/CLOSE")
  {
    printf("OFF A");
    analogWrite(5, 0);
    digitalWrite(0, LOW);
    
    printf("OFF B");
    analogWrite(4, 0);
    digitalWrite(2, LOW);
  }
}
