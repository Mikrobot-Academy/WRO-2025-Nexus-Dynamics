Team  NEXUS DYNAMICS – WRO 2025 Future Engineers
===========================================
Welcome to the official repository of Team NEXUS DYANMICS, proudly representing Mikrobot Academy from Ghana in the WRO 2025 Future Engineers category.

![image](https://github.com/user-attachments/assets/aaf8859e-a785-4ffc-8ddb-c9662de4f2f8)                   ![image](https://github.com/user-attachments/assets/8abd6526-0eed-4adb-95cb-b1cffd24fcd1)


## Overview of our repository 📜
* `schemes`- contains the circuit diagram.
* `models` - includes all the 3d printed parts of the robot.
* `others`-  This is for other files which can be used to understand the making of the vehicle. 
* `src` - the codes for both challenges.
* `t-photos` - photos of the team one formal and a funny one.
* `v-photos` - photos of the robot.
* `video` - the link to our youtube channel where you can see our robot in action completing both challenges.
* `README.md` - Here's all our journey in the development of our robot here we explain every part of the robot making.


## Components 🧱
A list of all the electrical and mechanical components in the robot.

| <img src="https://github.com/user-attachments/assets/d3bbbc94-1d77-4a10-b388-3a382ea46a10" width="200"/> | <img width="200" src="https://github.com/user-attachments/assets/1f7f4e71-633a-43bf-a034-508f58afc7b3" /> | <img width="200" src="https://github.com/user-attachments/assets/07f7be05-0aba-44dc-a01c-495c691c86ff" /> |
| :------------: | :------------: | :------------: |
| [Raspberry Pi 5 x1](https://www.raspberrypi.com/products/raspberry-pi-5/) | [L298N Motor Driver x1](https://www.daakyetech.com/store/l298n-motor-driver-board-v1/) | [HC-SR04 x3](https://www.sparkfun.com/ultrasonic-distance-sensor-hc-sr04.html) |

| <img src="https://github.com/user-attachments/assets/36bb7814-cce9-4a1d-80c5-c2ed0bf1e556" width="200"/> | <img width="200" src="https://github.com/user-attachments/assets/a940516d-c541-49dd-beae-73ed81932b35" /> | <img src="https://github.com/user-attachments/assets/27275a5d-7776-4320-a44b-e7747f863906" width="200" /> |
| :------------: | :------------: | :------------: |
| [25GA-370 Gear Motor x1](https://www.okuelectronics.com/store/motors-pumps/25ga-370-gear-motor-12v-250rpm-with-4mm-shaft/) | [MG-996R Servo x1](https://www.okuelectronics.com/store/motors-pumps/servo-mg996r-13kg-360-degree-high-quality/) | [Power Bank x1](https://www.jumia.com.gh/oraimo-power-bank-10000mah-toast-22.5-byte-22.5w-black-290664811.html) |

| <img width="200" src="https://github.com/user-attachments/assets/c2b60d16-a2de-4dc1-843e-174c5aca7a27" /> | <img width="200" src="https://github.com/user-attachments/assets/0a98dfb7-4dd8-4513-bf5d-a83f09e9cb15" /> | <img width="200" src="https://github.com/user-attachments/assets/38586082-cbe9-4d74-bf22-e17e035c0b51" /> |
| :------------: | :------------: | :------------: |
| [LiPo Battery x1](https://www.hobbyrc.co.uk/gnb-2200mah-3s-110c-lipo-battery) | [Push Button x1](https://www.chinadaier.com/kd4-21-dpst-push-button-switch/) | [Jumper Wires x24](https://www.daakyetech.com/store/jumper-wires-40-20/) |

<br></br>

---
## Circuit Diagram
<p align=center>
  <img width="500" src="https://github.com/user-attachments/assets/e3bb7f8e-4d87-455e-90c7-fc9164317f7f" alt="Circuit Diagram"/>
</p>

This circuit diagram represents the connections of our robotic system.

<br></br>
---


## Robot Photos 📸
| <img src="https://github.com/user-attachments/assets/0617c0fc-2120-489a-832b-4bb3aa1f7d46" width="270" alt="Top" /> | <img src="https://github.com/user-attachments/assets/d6911a03-71c9-4f97-83f1-c4225fc712f9" alt="Right" width="270"/> | <img src="https://github.com/user-attachments/assets/0e628e8a-256b-4e8c-b257-f839c9fc83b9" alt="Front" width="270"/>
| :------------: | :------------: | :------------: |
| Top       | Right        | Front       |
| <img src="https://github.com/user-attachments/assets/7943466b-ff11-4398-a772-cc1a77d0d420" width="270" alt="Left"/> | <img src="https://github.com/user-attachments/assets/9727a26b-9c81-431b-9bb8-67605aea3c47" alt="Back" width="270"/>| <img alt="Bottom" src="https://github.com/user-attachments/assets/75fb4978-209d-4018-8544-fdebf3c1bdb7" width="270" /> |
| Left       | Back       | Bottom       |

<br></br>
---

## Raspberry Pi Robot Code Explanation (Open Challenge)

---

### Library Imports & GPIO Mode

```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
```

- `RPi.GPIO` lets the Raspberry Pi communicate with motors, servos, sensors, etc.
- `time` is used for delays while reading sensors and controlling motors.
- `GPIO.setmode(GPIO.BCM)` uses the GPIO pin numbering based on the Broadcom chip, not physical pin numbers.
- `GPIO.setwarnings(False)` hides warnings if GPIO was used before.

---

### Button Setup (to select mode)

```python
BUTTON_PIN = 12
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
```

- Button is connected to GPIO 12
- Internal resistor is set to Pull-Down → button reads 0 until pressed

---

### Two Main Modes

| Code Function | Wall followed | Sensor pins | PID Tuning | Speed Setting |
|--------------|---------------|-------------|------------|--------------|
| `run_right_wall()` | Right wall | TRIG=7, ECHO=16 | Kd = 0.2 | 75% |
| `run_left_wall()` | Left wall | TRIG=25, ECHO=8 | Kd = 0.4 | 65% |

Different tuning because:
- Sensor placement and servo direction are opposite each side
- Gives smoother driving when tuned separately

---

### Ultrasonic Distance Measurement

```python
def read_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.00001)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Echo timing calculation here...
    duration = pulse_end - pulse_start
    distance = round(duration * 17150, 2)
```

- Calculates distance using time of sound returning
- `distance (cm) = duration × 17150`
- Returns `None` if ultrasonic reading fails

Used for detecting walls and corners.

---

### PID Steering Control

```python
Kp, Ki, Kd = 6, 0, 0.2
error = setpoint - d
correction = Kp*error + Ki*integral + Kd*derivative
servo_angle = 90 + correction
```

- Target distance from wall = 20 cm
- Too far → turn towards the wall
- Too close → turn away

Servo movement limits:

```python
angle = max(60, min(120, angle))
```

Prevents over-steering.

---

### Motor Control

```python
motor_pwm.ChangeDutyCycle(speed)
GPIO.output(IN1, True)
GPIO.output(IN2, False)
```

- PWM controls speed
- Direction pins choose forward/backward movement

Forward, stop, and corner manoeuvres controlled here.

---

### Corner Detection

```python
if d > 100 or d < 0:
    print("Wall lost, corner")
    approach_wall()
    corner_count += 1
```

- If no wall detected → robot guesses corner
- Turns and realigns with next wall
- Stops after max corners reached (full lap)

---

### Cleanup

```python
GPIO.cleanup()
```

- Releases GPIO pins cleanly
- Prevents Raspberry Pi crashes next time script runs

---
