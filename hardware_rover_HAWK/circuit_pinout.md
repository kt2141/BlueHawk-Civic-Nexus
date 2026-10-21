# H.A.W.K. Rover Circuit Pinout (Arduino Uno R3)

## Controller + Motor Drive

- **Arduino Uno R3** as main microcontroller.
- **Adafruit Motor Shield (L293D)** for differential DC gear motor control.
  - Left motor -> M1
  - Right motor -> M2

## Sensor Pin Mapping

- **HC-SR04 Ultrasonic**
  - VCC -> 5V
  - GND -> GND
  - TRIG -> D8
  - ECHO -> D7
- **IR Left line/proximity sensor** -> A0
- **IR Right line/proximity sensor** -> A1
- **UV sensor analog output** -> A2
- **Servo (sensor mast sweep)** signal -> D9

## Power Management

- Battery: **11.1V Li-Ion (3S)** pack.
- Rail strategy:
  - 11.1V battery -> motor power input (shield VIN, per shield limits).
  - Buck converter #1 -> regulated 5V for Arduino + sensors.
  - Buck converter #2 (optional isolated rail) -> edge compute module.
- All grounds must be common across Arduino, shield, sensors, and edge compute.

## Edge Compute Integration (ESP32-CAM / Raspberry Pi Zero 2W)

- Edge camera and YOLO/OpenCV processing run on ESP32-CAM or Raspberry Pi Zero 2W.
- Serial/UART bridge recommendation:
  - Arduino TX/RX <-> edge node RX/TX via level-safe interface.
- Exposed rover telemetry packet fields:
  - `state`, `distance_cm`, `ir_left`, `ir_right`, `uv`
- Edge module appends CV detections (bounding boxes/class/confidence) and GPS geotags before upstream publish.

## Wiring Notes

- Keep ultrasonic and servo wiring away from motor power lines to reduce noise.
- Add decoupling capacitors close to sensor rails.
- Verify motor shield current limits against stall current of selected DC gear motors.
