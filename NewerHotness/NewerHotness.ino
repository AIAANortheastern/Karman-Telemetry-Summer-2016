/*
 Name:		NewerHotness.ino
 Created:	8/2/2016 7:40:04 PM
 Author:	Andrew
*/

#include "Thermocouple_Max31855.h"
//#include <Adafruit_MAX31855.h>
#include <string.h>
#include <SPI.h>

#define DATA_SIZE           (4)
#define NUM_DATA            (3)
#define NUM_BYTES_TO_SEND   (16)
#define TEMP_0_INDEX        (0)
#define TEMP_1_INDEX        (4)
#define TEMP_2_INDEX        (8)

#define XBEE_PORT (Serial1)
#define XBEE_BAUD_RATE (57600)
#define XBEE_CONFIG (SERIAL_8N1)

#define CS_TCA1 (4)

#define TEMP1_BITMASK (0x8000)
#define TEMP2_BITMASK (0x4000)
#define TEMP3_BITMASK (0x2000)

#define FALSE false
#define TRUE true

#define XBEE_CTS_PIN        (6)

#define DEBUG_MODE

SPISettings SPI_TCA1(1000000, MSBFIRST, SPI_MODE0);


// XBEE TX_1 = Pin 1		Purple 7 on logic analyzer
// XBEE RX_1 = Pin 0		Blue 6  on logic analyzer

//SPI Clk Pin 13
//SPI DataOut Pin 11
//SPI DataIn Pin 12

//SPI Clock speed max ~1-2 MHz (4 for yolo)

typedef struct {
	float temp1;
	float temp2;
	float temp3;
	short poll_flags;
	short padding;
}send_data_t;

send_data_t gSendData;

const byte min_millis_btwn_send = 40;

byte send_string[sizeof(send_data_t) / sizeof(byte)];
elapsedMillis sinceSend;

// Call hardware spi constructor for TC1
Thermocouple_Max31855 thermocouple1(CS_TCA1, SPI_TCA1);


void setup() {
	//setup sensors and get ready for transmit loop
	//Configure Serial1
	XBEE_PORT.begin(XBEE_BAUD_RATE, XBEE_CONFIG);

	SPI.begin();


}

void loop()
{
	//get data and try to send after each check

	(void)get_temperature(1);
	//Try to send data
	send_check();

	(void)get_temperature(2);

	send_check();

	(void)get_temperature(3);

	send_check();



}


//test comment





void send_check()
{
	if (sinceSend > min_millis_btwn_send && digitalRead(XBEE_CTS_PIN) == LOW)
	{
		int numBytes = sizeof(send_string) / sizeof(byte);
		float debugFloat;
		memcpy(send_string, &gSendData, numBytes);
		XBEE_PORT.write(send_string, NUM_BYTES_TO_SEND); 
		for (int i = 0; i < numBytes / 4; i++)
		{
			memcpy(&debugFloat, (&send_string[4 * i]), 4);
			Serial.print(debugFloat);
			Serial.print('\n');
		}
		Serial.print(gSendData.poll_flags);
		Serial.print('\n');
		sinceSend = 0;
		gSendData.poll_flags &= 0;
	}
	return;

}

bool get_temperature(byte temp_number)
{
	bool retVal = false;
	//TODO get the temp
	//gSendData.temp<N> = getMyDataPls();
	switch (temp_number)
	{
	case 1:
		//Serial.println(thermocouple1.readInternal());
		thermocouple1.getTemperature(gSendData.temp1);
		gSendData.poll_flags |= TEMP1_BITMASK;
		retVal = true;
		break;
	case 2:
		gSendData.temp2 = 6.28;
		gSendData.poll_flags |= TEMP2_BITMASK;
		retVal = true;
		break;
	case 3:
		gSendData.temp3 = 9.42;
		gSendData.poll_flags |= TEMP3_BITMASK;
		retVal = true;
		break;
	default:
		break;
	}
	return retVal;
}



