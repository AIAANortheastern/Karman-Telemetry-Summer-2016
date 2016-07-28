#include <string.h>

#define DATA_SIZE           4
#define NUM_DATA            3
#define NUM_BYTES_TO_SEND   12
#define TEMP_0_INDEX        0
#define TEMP_1_INDEX        4
#define TEMP_2_INDEX        8


#define TEMP1_BITMASK (0x8000)
#define TEMP2_BITMASK (0x4000)
#define TEMP3_BITMASK (0x2000)

#define FALSE false
#define TRUE true

#define XBEE_CTS_PIN        6

#define DEBUG_MODE


typedef struct {
  float temp1;
  float temp2;
  float temp3;
  short poll_flags;
  short padding;
}send_data_t;

send_data_t gSendData;

const byte min_millis_btwn_send = 40;

byte send_string[sizeof(send_data_t)/sizeof(byte)];
/*
int read_num = 0;
*/
elapsedMillis sinceSend;
/*
union Data {
   double d_data;
   byte b_data[DATA_SIZE];
};*/

void setup() {
  //setup sensors and get ready for transmit loop
  
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

void send_check()
{ 
  if(sinceSend > min_millis_btwn_send && digitalRead(XBEE_CTS_PIN) == LOW)
  {
    int numBytes = sizeof(send_string)/sizeof(byte);
    float debugFloat;
    memcpy(send_string, &gSendData, numBytes);
    //Serial1.write(send_string, NUM_BYTES_TO_SEND); 
    for(int i = 0; i < numBytes/4; i++)
    {
      memcpy(&debugFloat, (&send_string[4*i]), 4);
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
  switch(temp_number)
  {
    case 1:
      gSendData.temp1 = 3.14;
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
