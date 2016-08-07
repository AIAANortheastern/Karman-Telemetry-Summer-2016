/*
 Name:      NewerHotness.ino
 Created:   8/2/2016 7:40:04 PM
 Author:    Andrew Kaster
*/

#include "Thermocouple_Max31855.h"
#include <string.h>
#include <SPI.h>
#include <SD.h>
#include <Time.h>
#include <TimeLib.h>

#define DATA_SIZE           (4)
#define NUM_DATA            (3)
#define NUM_BYTES_TO_SEND   (16) // TODO: Update this every time new sensor is added
#define TEMP_0_INDEX        (0)
#define TEMP_1_INDEX        (4)
#define TEMP_2_INDEX        (8)

#define XBEE_PORT           (Serial1)
#define XBEE_BAUD_RATE      (57600)
#define XBEE_CONFIG         (SERIAL_8N1)

#define CS_TCA1             (4)
#define XBEE_CTS_PIN        (6)
#define CS_SDCARD           (8) // TODO put proper pin for SD card chip select

#define TEMP1_BITMASK       (0x8000)
#define TEMP2_BITMASK       (0x4000)
#define TEMP3_BITMASK       (0x2000)
#define ACCEL_X_BITMASK     (0x1000)
#define ACCEL_Y_BITMASK     (0x0800)
#define ACCEL_Z_BITMASK     (0x0400)
#define ROLL_BITMASK        (0x0200)
#define PITCH_BITMASK       (0x0100)
#define YAW_BITMASK         (0x0080)

#define MILIS_BTWN_SEND     (40)
#define MILIS_BTWN_WRITE    (100)

#define DEBUG_MODE

// XBEE TX_1 = Pin 1        Purple 7 on logic analyzer
// XBEE RX_1 = Pin 0        Blue 6  on logic analyzer

//SPI Clk Pin 13
//SPI DataOut Pin 11
//SPI DataIn Pin 12

//SPI Clock speed max ~1-2 MHz (4 for yolo)

struct send_data_s {
    float temp1;
    float temp2;
    float temp3;
    short poll_flags;
    short padding;
};

typedef struct send_data_s send_data_t;

send_data_t gSendData;
byte send_string[sizeof(send_data_t) / sizeof(byte)];
String write_string;
File data_file;
elapsedMillis sinceSend;
elapsedMillis sinceWrite;
time_t currTime = now();

SPISettings SPI_TCA1(1000000, MSBFIRST, SPI_MODE0);

// Call hardware spi constructor for TC1
Thermocouple_Max31855 thermocouple1(CS_TCA1, SPI_TCA1);


void setup() {

    //setup sensors and get ready for transmit loop
    //Configure Serial1
    XBEE_PORT.begin(XBEE_BAUD_RATE, XBEE_CONFIG);

    SPI.begin();

    // setup SD card recording.
    // Note begin() uses the SPI interface
    // to do setup communications with the sd card.
    pinMode(CS_SDCARD, OUTPUT);
    if (!SD.begin(CS_SDCARD)) {
        Serial.println("Failed to Initialize SD card");
    }
}

void loop()
{
    //get data and try to send after each check

    (void)get_temperature(1);
    //Try to send data
    send_check();
    //Try to write data
    write_check();

    (void)get_temperature(2);

    send_check();
    write_check();

    (void)get_temperature(3);

    send_check();
    write_check();

}


void send_check()
{
    if (sinceSend > MILIS_BTWN_SEND && digitalRead(XBEE_CTS_PIN) == LOW)
    {
        int numBytes = sizeof(send_string) / sizeof(byte);
        memcpy(send_string, &gSendData, numBytes);
        XBEE_PORT.write(send_string, NUM_BYTES_TO_SEND);
#ifdef DEBUG_MODE
        float debugFloat;
        for (int i = 0; i < numBytes / 4; i++)
        {
            memcpy(&debugFloat, (&send_string[4 * i]), 4);
            Serial.print(debugFloat);
            Serial.print('\n');
        }
        Serial.print(gSendData.poll_flags);
        Serial.print('\n');
        sinceSend = 0;
#endif
        gSendData.poll_flags &= 0; //Clear flags
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



// Records all data currently in the global data structure to the SD card
// With a timestamp instead of poll flags
void write_check()
{
    if (sinceWrite > MILIS_BTWN_WRITE)
    {
        if (SD.exists("data.csv"))
        {
            data_file = SD.open("data.csv", FILE_WRITE);
            if (data_file)
            {
                currTime = now();
                write_string = String(currTime) + ',' + String(gSendData.temp1) + ',' + String(gSendData.temp2) + ',' \
                    + String(gSendData.temp3); // Add additional data to be logged here
#ifdef DEBUG_MODE
                Serial.println(String("SD card Data: \n" + write_string));
#endif
                data_file.println(write_string);
                data_file.close();
            }
            else
            {
                Serial.println("Error opening data file");
            }
        }
        else
        {
            Serial.println("Error finding data file");
        }
        sinceWrite = 0;
    }
}
