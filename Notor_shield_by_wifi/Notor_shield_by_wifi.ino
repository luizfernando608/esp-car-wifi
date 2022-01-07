#include "ESP_MICRO.h"

#define LED 16

void setup()
{
  servo_vertical.attach(0);  // attaches the servo on pin 9 to the servo object
  servo_horizontal.attach(2);  
  servo_vertical.write(5.0);
  servo_horizontal.write(5.0);
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

  float horizontal_move= (((String(url).substring(7,10)).toFloat())/9.9)*180;
  float vertical_move= (((String(url).substring(11,14)).toFloat())/9.9)*180;
  Serial.println(horizontal_move);
  Serial.println(vertical_move);
  

  servo_vertical.write(horizontal_move);
  
  servo_horizontal.write(vertical_move);  
  delay(50);

  if(L_direction == "-"){
    Serial.println("Frente");
    analogWrite(5, L_power);
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
