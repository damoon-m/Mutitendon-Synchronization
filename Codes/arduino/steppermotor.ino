#include <Arduino.h>
#include "A4988.h"

// using a 200-step motor (most common)
#define MOTOR_STEPS 200
// configure the pins connected
#define DIR 8
#define STEP 9
#define MS1 10
#define MS2 11
#define MS3 12
A4988 stepper(MOTOR_STEPS, DIR, STEP, MS1, MS2, MS3);

String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete

void setup() {
   // Set target motor RPM to 1RPM and microstepping to 1 (full step mode)
   stepper.begin(10, 16);

  // initialize serial:
  Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
}  

void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    Serial.println(inputString.toInt());
    stepper.rotate(inputString.toInt());
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
//    // Tell motor to rotate 360 degrees. That's it.
//    delay(3000);
//    stepper.rotate(60);
//    delay(3000);
//    stepper.rotate(-100);
}


/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
