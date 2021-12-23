//Programa: NodeMCU ESP8266 Motor Driver Shield
//Autor: Arduino e Cia
void setup()
{
  Serial.begin(9600);
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
  //Gira os motores no sentido horario
  //Aciona motor 1
  analogWrite(5, 1024); 
  digitalWrite(0, HIGH);  
  //Aciona motor 2
  analogWrite(4, 1024); 
  digitalWrite(2, HIGH); 
  //Aguarda 2 segundos
  delay(2000);
  //Gira os motores no sentido anti-horario
  //Aciona motor 1
  analogWrite(5, 1024); 
  digitalWrite(0, LOW); 
  //Aciona motor 2
  analogWrite(4, 1024); 
  digitalWrite(2, LOW); 
  //Aguarda 2 segundos e reinicia o processo
  delay(2000);
}
