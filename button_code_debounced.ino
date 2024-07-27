#include <SoftwareSerial.h>
#define BUTTON_PIN1 5  // Define the pin connected to the button
#define BUTTON_PIN2 9  // Define the second pin connected to the button
SoftwareSerial mySerial(2,4); //RX,TX -- -DONT CHANGE THIS or it doesn't work
SoftwareSerial mySerial2(7,6); //RX,TX -- -DONT CHANGE THIS or it doesn't work

char message1[] = "BUZZEDA*";// Change the letter depending on the arduino board used. 



int buttonState = HIGH;         // Current state of the button1
int lastButtonState = HIGH;    // Previous state of the button1




void setup()
{
  pinMode(BUTTON_PIN, INPUT_PULLUP); // Set button pin as input with pull-up resistor

  mySerial.begin(9600);
  Serial.begin(9600); // Initialize serial communication
}
 
void loop() // run over and over
{

  int buttonState = digitalRead(BUTTON_PIN1); // Read the state of the button
  
  if (buttonState == LOW && lastButtonState== HIGH) { // If button is pressed
  // Serial.println("Beep A");
    mySerial.print(message);
    
    delay(10);
    
  } 
  

lastButtonState1= buttonState1;


  
  
}



