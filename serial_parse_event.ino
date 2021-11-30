#include <SoftwareSerial.h>

SoftwareSerial mySerial(9,10); // RX, TX
String myString;

String last_message;

String buffer_message;
char a;

int Index1,Index2,Index3,Index4,Index5,Index6, Index7;
String secondValue, thirdValue, fourthValue, fifthValue, sixthValue, firstValue;
float pressure, o2, expiration;

bool stringComplete = false;

HardwareSerial Serial2(PD6, PD5);

void setup()
{
  // Open serial communications and wait for port to open:
  Serial.begin(115200);
  Serial2.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Native USB only
  }
  Serial.println("Goodnight moon!");
  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);
  mySerial.println("Hello, world?");
}

void loop() // run over and over
{
  SerialEvent2();  
  
    
  }

void SerialEvent2() {
  while (Serial2.available()) {
  if (Serial2.available() > 0){
    a = Serial2.read();
    myString += String(a);
    if (String(a) == "#"){
      Serial.println(myString);
      if (myString.length()>0) {
      Index1 = myString.indexOf('*');
      Index2 = myString.indexOf('|', Index1+1);
      Index3 = myString.indexOf('|', Index2+1);
      Index4 = myString.indexOf('|', Index3+1);
      Index5 = myString.indexOf('|', Index4+1);
      Index6 = myString.indexOf('|', Index5+1);
      Index7 = myString.indexOf('|', Index6+1);
      secondValue = myString.substring(Index1+1, Index2);
      thirdValue = myString.substring(Index2+1, Index3);
      fourthValue = myString.substring(Index3+1, Index4);
      fifthValue = myString.substring(Index4+1, Index5);
      sixthValue = myString.substring(Index5+1, Index6);
      firstValue = myString.substring(Index6+1, Index7);
      //Serial.println(Index1);
      pressure = secondValue.toFloat();
      Serial.print("pressure:");Serial.println(pressure);
      o2 = thirdValue.toFloat();
      Serial.print("o2:");Serial.println(o2);
      expiration = fourthValue.toFloat();      
      myString = "";
    }
     }  
    }
  }
}  
