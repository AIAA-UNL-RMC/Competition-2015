// Import the Arduino Servo library
#include <Servo.h> 
#include <Console.h>

// Create a Servo object for each servo
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
// Common servo setup values
int minPulse = 600;   // minimum servo position, us (microseconds)
int maxPulse = 2400;  // maximum servo position, us

// User input for servo and position
int userInput[3];    // raw input from serial buffer, 3 bytes
int startbyte;       // start byte, begin reading input
int servo;           // which servo to pulse?
int pos;             // servo angle 0-180
int i;               // iterator

/** Adjust these values for your servo and setup, if necessary **/
int servoPin; // control pin for servo motor
int refreshTime = 20; // time (ms) between pulses (50Hz)

/** The Arduino will calculate these values for you **/
int centerServo; // center servo position
int pulseWidth; // servo pulse width
int servoPosition; // commanded servo position, 0-180 degrees
int pulseRange; // max pulse - min pulse
long lastPulse = 0; // recorded time (ms) of the last pulse

void setup() 
{ 
  // Attach each Servo object to a digital pin
  servo1.attach(5, minPulse, maxPulse);
  servo2.attach(6, minPulse, maxPulse);
  servo3.attach(9, minPulse, maxPulse);
  servo4.attach(10, minPulse, maxPulse);
  servo5.attach(11, minPulse, maxPulse);

  // Open the serial connection, 9600 baud
  Serial.begin(9600);
  pinMode(13,OUTPUT);
  pinMode(8,OUTPUT);
  digitalWrite(13,LOW);
  Bridge.begin();
  digitalWrite(8,HIGH);
  Console.begin();
  while(!Console){} // Wait for console to connect
  digitalWrite(13,HIGH);
  pinMode(7,OUTPUT);
  digitalWrite(7,LOW);
  Serial.println("Slave Ready");
} 

void loop() 
{
  // Wait for serial input (min 3 bytes in buffer)
  if (Console.available() > 0) {
    int entry = Console.read();
    
    //Serial.println(shisnob);
    if (entry == 97){
      //Serial.println("shit");
      int servoNumber = Console.read();
      //Serial.print("C");
      //Serial.print(shisnoc);
      //Serial.println("");
     
      int servoID;
     
      // I doubt these are necessary; testing is again needed
      if (servoNumber == 49){
        servoPin = 5; // Drive1
      } else if (servoNumber == 50){
        servoPin = 6; // Drive2
      } else if (servoNumber == 51){
        servoPin = 9; // Screw
      } else if (servoNumber == 52){
        servoPin = 10; // Wheel
      } else if (servoNumber == 53){
        servoPin = 11; // Bucket
      }
	    
      // Get angle to write
      int pos = Console.read();
     
      if (servoNumber == 49){
        servo1.write(pos);
      } else if (servoNumber == 50){
        servo2.write(pos);
      } else if (servoNumber == 51){
        servo3.write(pos);
      } else if (servoNumber == 52){
        servo4.write(pos);
      } else if (servoNumber == 53){
        servo5.write(pos);
      }   
    }
  }
}
