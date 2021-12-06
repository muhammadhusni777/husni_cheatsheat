#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x3f, 16, 2);

char a;
String myString;
int stat;
unsigned long timer;
unsigned long prev_timer;
String message;
String message_prev;
int robot_state;

int servo1_deg;
int servo2_deg;
int servo3_deg;



void setup()
{

  servo1.attach(7);
  servo2.attach(8);
  servo3.attach(9);
	// initialize the LCD
 pinMode(13, OUTPUT);
	Serial.begin(9600);
	lcd.begin();

	// Turn on the blacklight and print a message.
	lcd.backlight();
	lcd.print("booting....");
  delay(3000);
  lcd.clear();
  lcd.noBacklight();
}

void loop()
{
	// Do nothing here...
 //SerialEvent();
 /*
 lcd.setCursor(0,0);
 lcd.print("Pyvoice Experiment");
 lcd.setCursor(0,1);
 lcd.print(myString);
*/
 stat = 0;
 
 timer = millis() - prev_timer;
 if (timer > 1000){
// Serial.print(stat);
// Serial.print(" ");
// Serial.print(myString);
// Serial.print(" ");
 Serial.println(message);
 prev_timer = millis();
 if (stat == 0){
  myString =" ";
 }
 }

 if (String(message) == " hurung"){
  digitalWrite(13, HIGH);
  lcd.backlight();
 }

 if (String(message) == " pareum"){
  digitalWrite(13, LOW);
  lcd.noBacklight();
 }

  if (String(message) == " hareup"){
  digitalWrite(13, LOW);
   servo1.write(90);
   servo2.write(90);
   servo3.write(90);
 }

 if (String(message) == " tukang"){
  digitalWrite(13, LOW);
   servo1.write(90);
   servo2.write(90);
   servo3.write(90);
 }

 if (String(message) == " nyapit"){
  digitalWrite(13, LOW);
   servo1.write(90);
   servo2.write(90);
   servo3.write(90);
 }

 if (String(message) == " lepas"){
  digitalWrite(13, LOW);
  servo1.write(90);
   servo2.write(90);
   servo3.write(90);
 }

 if (String(message) == " Luhur"){
  digitalWrite(13, LOW);
  servo1.write(90);
   servo2.write(90);
   servo3.write(90);
 }

 if (String(message) == " hapus"){
  digitalWrite(13, LOW);
  lcd.clear();
 }
  
if (String(message) != " hapus"){
  lcd.setCursor(0,0);
  lcd.print(message);
}

if (message_prev != message){
  lcd.clear();
}
  
  message_prev = message;
 
}


void serialEvent() {
  
  while (Serial.available()) {
    stat = 1;
  if (Serial.available() > 0){
    a = Serial.read();
    myString += String(a);
    message = myString;
     }
    // myString ="";  
    }
    //Serial.print(stat);
    //Serial.print(" ");
    //Serial.println(myString);
 
  }
