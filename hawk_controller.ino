/* 
 * Project H.A.W.K. - Autonomous Human-Tracking & Street Patrol Rover
 * Microcontroller: Arduino Uno R3 / Motor Shield Driver
 */

#include <Servo.h>

// Pin Definitions
const int RIGHT_PIN = A1;
const int LEFT_PIN = A2;
const int SERVO_PIN = 9;

// Constants
const int MOVE_DIST_MAX = 100; // cm
const int SENSOR_ACTIVE = LOW; // Active low IR
const int SERVO_CENTER = 90;
const int SERVO_LEFT = 145;
const int SERVO_RIGHT = 35;
const int BASE_SPEED = 180;
const int TURN_DIFF = 60;

Servo headServo;
int currentState = 0;
int lastState = -1;

void setup() {
  Serial.begin(9600);
  pinMode(RIGHT_PIN, INPUT);
  pinMode(LEFT_PIN, INPUT);
  headServo.attach(SERVO_PIN);
  headServo.write(SERVO_CENTER);
  stopAllMotors();
}

void loop() {
  evaluateState();
  applyState();
  delay(50);
}

void evaluateState() {
  int distance_cm = 45; // Simulated ultrasonic distance ping
  int Right_Value = digitalRead(RIGHT_PIN);
  int Left_Value = digitalRead(LEFT_PIN);

  if (distance_cm == 0 || distance_cm > MOVE_DIST_MAX) {
    currentState = 0; // STATE_STOP
    return;
  }

  bool rightActive = (Right_Value == SENSOR_ACTIVE);
  bool leftActive = (Left_Value == SENSOR_ACTIVE);

  if (rightActive && leftActive) {
    currentState = 2; // STATE_TURN_RIGHT
    return;
  }
  if (leftActive && !rightActive) {
    currentState = 1; // STATE_TURN_LEFT
    return;
  }
  currentState = 3; // STATE_FORWARD
}

void applyState() {
  if (currentState == lastState) return;
  switch (currentState) {
    case 0: // STOP
      stopAllMotors();
      headServo.write(SERVO_CENTER);
      break;
    case 3: // FORWARD
      headServo.write(SERVO_CENTER);
      setForward();
      break;
    case 1: // TURN LEFT
      headServo.write(SERVO_LEFT);
      break;
    case 2: // TURN RIGHT
      headServo.write(SERVO_RIGHT);
      break;
  }
  lastState = currentState;
}

void stopAllMotors() {
  // Motor stop routine placeholder
}

void setForward() {
  // Motor forward routine placeholder
}
