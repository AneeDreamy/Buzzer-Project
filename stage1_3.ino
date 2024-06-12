#include <SoftwareSerial.h>
#define BUTTON_PIN 12  // Define the pin connected to the button
SoftwareSerial mySerial(2,4); //RX,TX -- -DONT CHANGE THIS or it doesn't work

char message[] = "BUZZED*";

void setup()
{
  pinMode(BUTTON_PIN, INPUT_PULLUP); // Set button pin as input with pull-up resistor
  mySerial.begin(9600);
  Serial.begin(9600); // Initialize serial communication
}
 
void loop() // run over and over
{

  int buttonState = digitalRead(BUTTON_PIN); // Read the state of the button
  
  
  if (buttonState == LOW) { // If button is pressed
    mySerial.print(message);
    delay(10);
    Serial.print()
    
  } 
  


  delay(150); // Add a small delay to debounce the button
  
  
}



