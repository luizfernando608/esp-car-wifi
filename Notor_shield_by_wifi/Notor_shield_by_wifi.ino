#include "ESP_MICRO.h"
#include <Servo.h>
#include <cstdlib>
#define LED 16

Servo servo_vertical;  // create servo object to control a servo
Servo servo_horizontal;

// The power of
String url;
float L_power;
String L_direction;
float R_power;
String R_direction;
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
  // Getting the request
  url = getPath();
  // format /+0/+0/0.0/0.0
  // Varia de 0 a 9
  // Getting the power of each wheel
  L_power = ( float(String(url[2]).toInt())/9)*1024 ;
  R_power = ( float(String(url[5]).toInt())/9)*1024 ;
  // Getting the di
  L_direction = String(url[1]);
  R_direction = String(url[4]);

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
  }
  else if(L_direction == "+"){
    Serial.println("re");
    analogWrite(5, L_power); 
   digitalWrite(0, HIGH); 
  }
  if(R_direction == "-"){
    Serial.println("Frente");
    analogWrite(4, R_power);
   digitalWrite(2, HIGH);
  }
  else if(R_direction == "+"){
    Serial.println("re");
    analogWrite(4, R_power); 
   digitalWrite(2, LOW); 
  }

  
  
  

}

