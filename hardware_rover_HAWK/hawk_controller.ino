#include <AFMotor.h>
#include <Servo.h>

enum RoverState {
  STATE_STOP,
  STATE_FORWARD,
  STATE_TURN_LEFT,
  STATE_TURN_RIGHT
};

// Motor shield channels (L293D via Adafruit Motor Shield v1)
AF_DCMotor leftMotor(1, MOTOR12_1KHZ);
AF_DCMotor rightMotor(2, MOTOR12_1KHZ);

// HC-SR04 pins
const int PIN_TRIG = 8;
const int PIN_ECHO = 7;

// IR sensors (left/right)
const int PIN_IR_LEFT = A0;
const int PIN_IR_RIGHT = A1;

// UV sensor
const int PIN_UV = A2;

// Servo for sensor sweep (optional mounted ultrasonic)
const int PIN_SERVO = 9;
Servo scanServo;

RoverState currentState = STATE_STOP;

const int SPEED_FORWARD = 180;
const int SPEED_TURN = 160;
const float OBSTACLE_DISTANCE_CM = 25.0;
const int IR_DEVIATION_THRESHOLD = 600;
const int UV_ALERT_THRESHOLD = 700;

unsigned long lastTelemetryMs = 0;
const unsigned long TELEMETRY_INTERVAL_MS = 1000;

float readDistanceCm() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);

  long duration = pulseIn(PIN_ECHO, HIGH, 25000); // ~4m timeout
  if (duration == 0) {
    return 999.0;
  }
  return (duration * 0.0343) / 2.0;
}

void stopMotors() {
  leftMotor.setSpeed(0);
  rightMotor.setSpeed(0);
  leftMotor.run(RELEASE);
  rightMotor.run(RELEASE);
}

void driveForward() {
  leftMotor.setSpeed(SPEED_FORWARD);
  rightMotor.setSpeed(SPEED_FORWARD);
  leftMotor.run(FORWARD);
  rightMotor.run(FORWARD);
}

void turnLeft() {
  leftMotor.setSpeed(SPEED_TURN);
  rightMotor.setSpeed(SPEED_TURN);
  leftMotor.run(BACKWARD);
  rightMotor.run(FORWARD);
}

void turnRight() {
  leftMotor.setSpeed(SPEED_TURN);
  rightMotor.setSpeed(SPEED_TURN);
  leftMotor.run(FORWARD);
  rightMotor.run(BACKWARD);
}

void applyState(RoverState state) {
  switch (state) {
    case STATE_STOP:
      stopMotors();
      break;
    case STATE_FORWARD:
      driveForward();
      break;
    case STATE_TURN_LEFT:
      turnLeft();
      break;
    case STATE_TURN_RIGHT:
      turnRight();
      break;
  }
}

RoverState evaluateState(float distanceCm, int irLeft, int irRight) {
  if (distanceCm < OBSTACLE_DISTANCE_CM) {
    return (irLeft > irRight) ? STATE_TURN_RIGHT : STATE_TURN_LEFT;
  }

  bool leftOffTrack = irLeft > IR_DEVIATION_THRESHOLD;
  bool rightOffTrack = irRight > IR_DEVIATION_THRESHOLD;

  if (leftOffTrack && !rightOffTrack) {
    return STATE_TURN_RIGHT;
  }
  if (rightOffTrack && !leftOffTrack) {
    return STATE_TURN_LEFT;
  }

  return STATE_FORWARD;
}

void setup() {
  Serial.begin(115200);

  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  pinMode(PIN_IR_LEFT, INPUT);
  pinMode(PIN_IR_RIGHT, INPUT);
  pinMode(PIN_UV, INPUT);

  scanServo.attach(PIN_SERVO);
  scanServo.write(90);

  applyState(STATE_STOP);
}

void loop() {
  float distanceCm = readDistanceCm();
  int irLeft = analogRead(PIN_IR_LEFT);
  int irRight = analogRead(PIN_IR_RIGHT);
  int uvReading = analogRead(PIN_UV);

  RoverState nextState = evaluateState(distanceCm, irLeft, irRight);
  if (uvReading > UV_ALERT_THRESHOLD) {
    nextState = STATE_STOP;
  }

  if (nextState != currentState) {
    currentState = nextState;
    applyState(currentState);
  } else {
    applyState(currentState);
  }

  if (millis() - lastTelemetryMs >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryMs = millis();
    Serial.print("state=");
    Serial.print((int)currentState);
    Serial.print(",distance_cm=");
    Serial.print(distanceCm);
    Serial.print(",ir_left=");
    Serial.print(irLeft);
    Serial.print(",ir_right=");
    Serial.print(irRight);
    Serial.print(",uv=");
    Serial.println(uvReading);

    if (uvReading > UV_ALERT_THRESHOLD) {
      Serial.println("anomaly=uv_environment_alert");
    }
  }

  delay(50);
}
