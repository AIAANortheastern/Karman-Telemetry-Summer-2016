#include <SPI.h>

void setup() {
  // put your setup code here, to run once:
    pinMode(10, OUTPUT);
    Serial.begin(9600);
    Serial.print("Begin\n");
    digitalWrite(10, HIGH);
    delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned int retVal;
  SPI.begin();
  SPI.beginTransaction(SPISettings(14000000, MSBFIRST, SPI_MODE1));
  digitalWrite(10, LOW);
  delay(500);
  retVal = SPI.transfer16(0);
  SPI.endTransaction();
  digitalWrite(10, HIGH);
  Serial.print(retVal/8);
  Serial.print("\n");
  delay(500);
}
