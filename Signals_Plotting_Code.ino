#include <Filters.h>

float Frequency_H = 2;
float Frequency_L = 25;
int valueecg=0;
int valueppg=0;
int filtered1=0;
int filtered2=0;
  

FilterOnePole filterOneHighpass( HIGHPASS, Frequency_H );
FilterOnePole filterOneLowpass( LOWPASS, Frequency_L );
void setup() {
  // put your setup code here, to run once:

  Serial.begin( 9600 );    // start the serial port
  pinMode(5, INPUT); // Setup for leads off detection LO +
  pinMode(6, INPUT); // Setup for leads off detection LO -
  
}

void loop() {
//  if((digitalRead(5) == 1)||(digitalRead(6) == 1)){
//Serial.println('!');
//}
//else{
  // put your main code here, to run repeatedly:
  valueecg=analogRead(A0);
  valueppg=analogRead(A5);
  
  filterOneHighpass.input(valueecg);
  filtered1=filterOneHighpass.output();
  filterOneLowpass.input(filtered1);
  filtered2=filterOneLowpass.output();
  String data = String(valueppg)+","+String((filtered2+200)*4);
 Serial.println(data);
 //delay(20);
 // Serial.print("IN:");
 //   Serial.print(valueppg);
 //   Serial.print(",");
 // Serial.print("Out:");
 //   Serial.println((filtered2+200)*4);

 // }
     
}
