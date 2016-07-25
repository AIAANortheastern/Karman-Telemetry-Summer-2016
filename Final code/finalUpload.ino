#include <SPI.h>
#include <SD.h>

// GPS is 3 floats, lat, long, speed (GMT and date optional)
const int thermoSelect1 = 20;

void setup() {
  pinMode (thermoSelect1,OUTPUT);
  spi.begin();
  // Serial1 = Strat
  Serial1.begin(9600)
  // Serial2 = GPS
  Serial2.begin(9600)
  // Serial3 = Xbee
  Serial2.begin(9600)

}



float getThermo(cs){
    // spi read via supplied cs
}

float getAcc(x=true, y= true, x = true) {
    // get acceleromiter from x,y,z if true
}

float readSL(){
    if (Serial1.avalable() > 0)
    {
        incomingByte = Serial1.read();
    }
}













void loop() {
    getData();
    sendData();  
}