//--------------------------------------------------------------------------
// Code to test basic Hapkit functionality (sensing and force output)
// Updated by Allison Okamura 1.17.2018
//--------------------------------------------------------------------------

// Includes
#include <math.h>

// Pin declares
int pwmPin = 5; // PWM output pin for motor 1
int dirPin = 8; // direction output pin for motor 1
int sensorPosPin = A2; // input pin for MR sensor
int fsrPin = A3; // input pin for FSR sensor

// Pins added for vibration motors
int pinL = 11; // pin for vibration motor on left side of steering wheel
int pinR = 3; // pin for vibration motor on right side of steering wheel

double dutyL = 0; // duty cycle for left vibration motor
double dutyR = 0; // duty cycle for right vibration motor
double motor_state = 0; // track if vibration motors are on or off

unsigned long previousMillis = 0;  // will store last time vibration motors were updated
long interval = 0;
int max_vibration_timing = 30000; // maximum vibration timing (milliseconds)
int min_vibration_timing = 15000; // minimum vibration timing (milliseconds)


// Position tracking variables
int updatedPos = 0;     // keeps track of the latest updated value of the MR sensor reading
int rawPos = 0;         // current raw reading from MR sensor
int lastRawPos = 0;     // last raw reading from MR sensor
int lastLastRawPos = 0; // last last raw reading from MR sensor
int flipNumber = 0;     // keeps track of the number of flips over the 180deg mark
int tempOffset = 0;
int rawDiff = 0;
int lastRawDiff = 0;
int rawOffset = 0;
int lastRawOffset = 0;
const int flipThresh = 700;  // threshold to determine whether or not a flip over the 180 degree mark occurred
boolean flipped = false;
double OFFSET = 980;
double OFFSET_NEG = 15;

// Kinematics variables
double xh = 0;           // position of the handle [m]

// Force output variables
double force = 0;           // force at the handle
double Tp = 0;              // torque of the motor pulley
double duty = 0;            // duty cylce (between 0 and 255)
unsigned int output = 0;    // output command to the motor

String command;

// --------------------------------------------------------------
// Setup function -- NO NEED TO EDIT
// --------------------------------------------------------------
void setup() 
{
  // Set up serial communication
  Serial.begin(250000);
  
  // Set PWM frequency 
  setPwmFrequency(pwmPin,1); 
  
  // Input pins
  pinMode(sensorPosPin, INPUT); // set MR sensor pin to be an input
  pinMode(fsrPin, INPUT);       // set FSR sensor pin to be an input

  // Output pins
  pinMode(pwmPin, OUTPUT);  // PWM pin for motor A
  pinMode(dirPin, OUTPUT);  // dir pin for motor A
  
  // Initialize motor 
  analogWrite(pwmPin, 0);     // set to not be spinning (0/255)
  digitalWrite(dirPin, LOW);  // set direction
  
  // Initialize position valiables
  lastLastRawPos = analogRead(sensorPosPin);
  lastRawPos = analogRead(sensorPosPin);
  flipNumber = 0;

  // Set PWM frequencies
  setPwmFrequency(pinL, 1);
  setPwmFrequency(pinR, 1);

  // Output pins
  pinMode(pinL, OUTPUT); // PWM pin for left vibration motor
  pinMode(pinR, OUTPUT); // PWM pin for right vibration motor

  // Initialize motors
  analogWrite(pinL, 0); 
  analogWrite(pinR, 0); 
}


// --------------------------------------------------------------
// Main Loop
// --------------------------------------------------------------
void loop()
{
  
  //*************************************************************
  //*** Section 1. Compute position in counts (do not change) ***  
  //*************************************************************

  // Get voltage output by MR sensor
  rawPos = analogRead(sensorPosPin);  //current raw position from MR sensor

  // Calculate differences between subsequent MR sensor readings
  rawDiff = rawPos - lastRawPos;          //difference btwn current raw position and last raw position
  lastRawDiff = rawPos - lastLastRawPos;  //difference btwn current raw position and last last raw position
  rawOffset = abs(rawDiff);
  lastRawOffset = abs(lastRawDiff);
  
  // Update position record-keeping vairables
  lastLastRawPos = lastRawPos;
  lastRawPos = rawPos;
  
  // Keep track of flips over 180 degrees
  if((lastRawOffset > flipThresh) && (!flipped)) { // enter this anytime the last offset is greater than the flip threshold AND it has not just flipped
    if(lastRawDiff > 0) {        // check to see which direction the drive wheel was turning
      flipNumber--;              // cw rotation 
    } else {                     // if(rawDiff < 0)
      flipNumber++;              // ccw rotation
    }
    flipped = true;            // set boolean so that the next time through the loop won't trigger a flip
  } else {                        // anytime no flip has occurred
    flipped = false;
  }
   updatedPos = rawPos + flipNumber*OFFSET; // need to update pos based on what most recent offset is 

 
  //*************************************************************
  //*** Section 2. Compute position in meters *******************
  //*************************************************************

  double rh = 0.09;   //[m]
  //double ts = updatedPos * -0.0122 + 12.1374; // Jerry's Hapkit 
  double ts = updatedPos * -0.0122 + 12; // Jerry's Hapkit 
  // double ts = -(0.0121 * updatedPos - 4.5246); // Johnny's Hapkit 
  double xh = ts * (M_PI/180) * rh;
  Serial.println(xh,5);

  //double k = 0.4; // spring force [N/m]
  double k = 0.6; // spring force [N/m]
  double max_duty = 0.5; // maximum possible duty cycle (within comfortable limit of the vibration motors)
  unsigned long currentMillis = millis(); // current time
  double depth; 
  double MAX_DEPTH;
  unsigned long random_force_counter = 0;
  double random_force = random(-100,100)/100.0;

  if(Serial.available()){
    random_force_counter += 1;
    command = Serial.readStringUntil('\n');
    // Parse and extract the two variables
    depth = command.substring(0, command.indexOf(',')).toDouble();
    String MAX_DEPTH2STRING = command.substring(command.indexOf(',') + 1);
    MAX_DEPTH2STRING.trim();
    MAX_DEPTH = MAX_DEPTH2STRING.toDouble();
    if(depth > 0){ // right crash, depth is positive value
      force = -k * depth;
      dutyR = 0.9;
      dutyL = 0;
    } else if(depth < 0){  // left crash, depth is negative value 
      force = -k * depth;
      dutyL = 0.7;
      dutyR = 0;
    } else {
      force = 0;
      dutyR = 0;
      dutyL = 0;
    }

    // editing for studies
    // force = 0;
    // dutyR = 0;
    // dutyL = 0;

    if (random_force_counter > 200) {
      random_force = random(-100,100)/100.0;
      random_force_counter = 0;
    }
    force += random_force;
    interval = max_vibration_timing - (max_vibration_timing-min_vibration_timing)*(abs(depth)/MAX_DEPTH);
    interval = max(0, interval);
  }

  int outputL = (int)(dutyL * 255);
  int outputR = (int)(dutyR * 255);
  double offset = 1.5; 

  // if ((abs(depth) + offset) >= MAX_DEPTH) {
  //   // analogWrite(pinL, outputL);
  //   // analogWrite(pinR, outputR);
  // }

  if (currentMillis - previousMillis >= interval) {
    // save the last time you turned the vibration motors on/off
    previousMillis = currentMillis;

    // if the motor is off turn it on and vice-versa:
    if (motor_state == 0) {
      analogWrite(pinL, outputL);
      analogWrite(pinR, outputR);
      motor_state = 1;
    } else {
      analogWrite(pinL, 0);
      analogWrite(pinR, 0);
      motor_state = 0;
    }
  }

  //*************************************************************
  //*** Section 3. Assign a motor output force in Newtons *******  
  //*************************************************************
 
  double rp = 0.0047625;   //[m]
  double rs = 0.075;   //[m] 
  double Tp = force * ((rh * rp)/rs); 
 
  //*************************************************************
  //*** Section 4. Force output (do not change) *****************
  //*************************************************************
  
  // Determine correct direction for motor torque
  if(force > 0) { 
    digitalWrite(dirPin, HIGH);
  } else {
    digitalWrite(dirPin, LOW);
  }

  // Compute the duty cycle required to generate Tp (torque at the motor pulley)
  duty = sqrt(abs(Tp)/0.0183);

  // Make sure the duty cycle is between 0 and 100%
  if (duty > 1) {            
    duty = 1;
  } else if (duty < 0) { 
    duty = 0;
  }  
  output = (int)(duty* 255);   // convert duty cycle to output signal
  analogWrite(pwmPin,output);  // output the signal
}

// --------------------------------------------------------------
// Function to set PWM Freq -- DO NOT EDIT
// --------------------------------------------------------------
void setPwmFrequency(int pin, int divisor) {
  byte mode;
  if(pin == 5 || pin == 6 || pin == 9 || pin == 10) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 64: mode = 0x03; break;
      case 256: mode = 0x04; break;
      case 1024: mode = 0x05; break;
      default: return;
    }
    if(pin == 5 || pin == 6) {
      TCCR0B = TCCR0B & 0b11111000 | mode;
    } else {
      TCCR1B = TCCR1B & 0b11111000 | mode;
    }
  } else if(pin == 3 || pin == 11) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 32: mode = 0x03; break;
      case 64: mode = 0x04; break;
      case 128: mode = 0x05; break;
      case 256: mode = 0x06; break;
      case 1024: mode = 0x7; break;
      default: return;
    }
    TCCR2B = TCCR2B & 0b11111000 | mode;
  }
}

