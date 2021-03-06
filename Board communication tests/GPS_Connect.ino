// $GPRMC,194509.000,A,4042.6142,N,07400.4168,W,2.03,221.11,160412,,,A*77
// GMT
// A/V (V = void, A = active / valid data)
// lat (NOT in decimal, has to be parced) DDMM.MMMM (+N -S)
// direction
// long DDDMM.MMMM
// direction (+E -W)
// Speed in knots
// current date DDMMYY
// Data transfer checksum
#include <Adafruit_GPS.h>

HardwareSerial mySerial = Serial1;
Adafruit_GPS GPS(&mySerial);

boolean usingInterrupt = true;
void useInterrupt(boolean);

void setup() {
  Serial.begin(115200);
  
  GPS.begin(9600)

   // uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // uncomment this line to turn on only the "minimum recommended" data
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);

    // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
  // For the parsing code to work nicely and have time to sort thru the data, and
  // print it out we don't suggest using anything higher than 1 Hz
  //RGPS.sendCommand(PMTK_SET_NMEA_UPDATE_10HZ);
  //GPS.sendCommand(PMTK_API_SET_FIX_CTL_5HZ);

    // Request updates on antenna status, comment out to keep quiet
    GPS.sendCommand(PGCMD_ANTENNA); 

    userInterrupt(true)
    delay(1000)
}

// Interrupt is called once a millisecond, looks for any new GPS data, and stores it
SIGNAL(TIMER0_COMPA_VECT){
    char c = GPS.read();
    // place to debug
    #ifdef UDR0
        if (GPSECHO)
            if (c) UDR0 = c;
        // writing direct to the udro is faster tahn serial print
        // only 1 character a a time can be written

}
