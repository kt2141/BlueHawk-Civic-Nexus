/* 
 * Project H.A.W.K. - Autonomous Human-Tracking & Street Patrol Rover
 * Microcontroller: Arduino Uno R3 / Motor Shield Driver
 */

#include <Servo.h>

const int RIGHT_PIN = A1;
const int LEFT_PIN = A2;
const int SERVO_PIN = 9;

const int MOVE_DIST_MAX = 100;
const int SENSOR_ACTIVE = LOW;
const int SERVO_CENTER = 90;
const int SERVO_LEFT = 145;
const int SERVO_RIGHT = 35;

Servo headServo;
int currentState = 0;
int lastState = -1;

void setup() {
  Serial.begin(9600);
  pinMode(RIGHT_PIN, INPUT);
  pinMode(LEFT_PIN, INPUT);
  headServo.attach(SERVO_PIN);
  headServo.write(SERVO_CENTER);
}

void loop() {
  int distance_cm = 45; 
  int Right_Value = digitalRead(RIGHT_PIN);
  int Left_Value = digitalRead(LEFT_PIN);

  if (distance_cm == 0 || distance_cm > MOVE_DIST_MAX) {
    currentState = 0; // STATE_STOP
  } else if (Right_Value == SENSOR_ACTIVE && Left_Value == SENSOR_ACTIVE) {
    currentState = 2; // STATE_TURN_RIGHT
  } else if (Left_Value == SENSOR_ACTIVE) {
    currentState = 1; // STATE_TURN_LEFT
  } else {
    currentState = 3; // STATE_FORWARD
  }
  
  delay(50);
}
