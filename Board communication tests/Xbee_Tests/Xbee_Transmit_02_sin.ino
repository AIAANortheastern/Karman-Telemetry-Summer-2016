/*
void setup() {
  Serial.begin(9600);
}
void loop(){
    Serial.println("This is my world!");
    delay(2000);
}
*/
String Data,startChar,delim,endChar,dataOne,dataTwo;
int d1 = 0;
int d2 = 0;
int dat1 = 0;
int dat2 = 0;
float pi = 3.14159;
void setup() {
  Serial.begin(9600);
  while (!Serial){;}
    // waits for serial to start
  Data = String();
  startChar = String("/");
  delim = String("^");
  endChar = String(";\n");
  dataOne = String("Data_One:");
  dataTwo = String("Data_Two:");
}



void loop() {
    d1 +=1;
    dat1 = d1 % 50;
    d2 +=1;
    dat2 = (d2 % 35);
    dataOne += dat1;
    dataTwo += dat2;
    // portOne.listen();
    // Serial.println("data...");
    // while (portTwo.avaliable() > 0){
    // Serial.write("c");}
    String TCdata = "This Data";
    Data += startChar;
    Data += dataOne;
    Data += delim;
    Data += dataTwo;
    Data += endChar;
    Serial.print(Data);
    //SDport.println(Data);
    Data = String();
    dataOne = String("Data_One:");
    dataTwo = String("Data_Two:");

//    delay(1000);
      delay(50);
}



