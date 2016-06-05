#include <SPI.h>
#include <MAX6675.h>
SS = 10
DO = 12
CLK = 13

MAX6675 thermocouple(CLK,SS,DO)

void setup() {
  Serial.begin(9600);
  SPI.begin();
  pinMode(SS,OUTPUT);
  delay(500);
}

/* 
K type thermocouple conversion
cold junction compensation
VOUT = (41µV / °C) 5 (TR - TAMB)

prints a 12bit sequence, all 0s is 0c, all 1s is 1023.75
reads take 16 complete clock cycles
qseuence:
d15: dummy sign and is always 0
D14-D3 converted temperature in order of MSB to LSB
D2 normally low and goes high when TC input is open
D1 is low to provide device ID
D0 is three state

t- must be grounded for D2 to be low and the TC to work

*/

double readCelsius(int cs){
  // This function reads the temp in C for the specified TC
  // cs in this case is the chip select pin for the specified TC
  uint16_t v;
  digitalWrite(cs,LOW);
  delay(1);

  v = spiread();
  v <<= 8; //Bitwise shift left 8 bits
  v |= spiread(); // bitwise or
  digitalWrite(cs,HIGH);

  if (v & 0x4){
    // Problem with the thermocouple
    return NAN;
  }
  v >>= 3; //betwise shift right 3
  return v*0.25;

}
// =====================================================================


 MAX6675::MAX6675(int8_t SCLK, int8_t CS, int8_t MISO) {
   sclk = SCLK;
   cs = CS;
   miso = MISO;
 
   //define pin modes
   pinMode(cs, OUTPUT);
   pinMode(sclk, OUTPUT); 
   pinMode(miso, INPUT);
 
   digitalWrite(cs, HIGH);
 }
 double MAX6675::readCelsius(void) {
 
   uint16_t v;
 
   digitalWrite(cs, LOW);
   _delay_ms(1);
 
   v = spiread();
   v <<= 8;
   v |= spiread();
 
   digitalWrite(cs, HIGH);
 
   if (v & 0x4) {
     // uh oh, no thermocouple attached!
     return NAN; 
     //return -100;
   }
 
   v >>= 3;
 
   return v*0.25;
 }
 
 double MAX6675::readFahrenheit(void) {
   return readCelsius() * 9.0/5.0 + 32;
 }
 
 byte MAX6675::spiread(void) { 
   int i;
   byte d = 0;
 
   for (i=7; i>=0; i--)
   {
     digitalWrite(sclk, LOW);
     _delay_ms(1);
     if (digitalRead(miso)) {
       //set the bit to 0 no matter what
       d |= (1 << i);
     }
 
     digitalWrite(sclk, HIGH);
     _delay_ms(1);
   }
 
   return d;
 }
// ====================================================================



void loop() {
  // digitalWrite(SS,HIGH)
  // delay(100)
  // read the sensor data
    float temp = thermocouple.readCelsius();
    Serial.print(temp);
    delay(5000);
}