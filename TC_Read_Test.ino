#include <SPI.h>
SS = 10
void setup() {
  Serial.begin(9600);
  SPI.begin();
  pinMode(SS,OUTPUT);
  delay(500)
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
void loop() {
  digitalWrite(SS,HIGH)
  delay(100)
  // read the sensor data
}