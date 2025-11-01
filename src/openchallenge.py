import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BUTTON_PIN = 12
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# ====================
# === RIGHT WALL (k.py)
# ====================
def run_right_wall():
    print("▶▶ Running RIGHT wall code...")

    # === GPIO SETUP ===
    TRIG = 7
    ECHO = 16
    SERVO_PIN = 18
    ENA = 22
    IN1 = 17
    IN2 = 27

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    GPIO.setup([ENA, IN1, IN2], GPIO.OUT)

    servo_pwm = GPIO.PWM(SERVO_PIN, 50)
    servo_pwm.start(7.5)
    motor_pwm = GPIO.PWM(ENA, 1000)
    motor_pwm.start(0)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)

    # PID constants
    Kp, Ki, Kd = 5, 0, 0.2
    setpoint = 20
    last_error, integral = 0, 0
    corner_count, max_corners = 0, 12

    def read_distance():
        GPIO.output(TRIG, False)
        time.sleep(0.00001)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        start = time.perf_counter()
        timeout = start + 0.04
        pulse_start, pulse_end = None, None
        while GPIO.input(ECHO) == 0 and time.perf_counter() < timeout:
            pulse_start = time.perf_counter()
        while GPIO.input(ECHO) == 1 and time.perf_counter() < timeout:
            pulse_end = time.perf_counter()
        if pulse_start and pulse_end:
            duration = pulse_end - pulse_start
            distance = round(duration * 17150, 2)
            if distance <= 0: return -1
            if distance > 600: return None
            return distance
        return None

    def set_servo_angle(angle):
        angle = max(60, min(120, angle))
        duty = 2 + (angle / 18)
        servo_pwm.ChangeDutyCycle(duty)
        print(f"Servo → {angle:.2f}°")

    def stop_robot():
        motor_pwm.ChangeDutyCycle(0)
        GPIO.output(IN1, False)
        GPIO.output(IN2, False)
        set_servo_angle(90)
        print("🚦 Stopped")

    def start_robot(speed=75):
        motor_pwm.ChangeDutyCycle(speed)
        GPIO.output(IN1, True)
        GPIO.output(IN2, False)
        print(f"🚀 Forward {speed}")

    def approach_wall():
        set_servo_angle(60)
        start_robot(74)
        while True:
            d = read_distance()
            if d and d > 0 and d < 50:
                stop_robot()
                print(f"✅ Found wall {d:.2f}cm")
                break
            time.sleep(0.02)

    try:
        while corner_count < max_corners:
            d = read_distance()
            if d is None: continue
            if d > 100 or d < 0:
                start_time = time.perf_counter()
                stop_robot()
                print(f"⚠️ Wall lost, corner {corner_count+1}")
                approach_wall()
                elapsed = time.perf_counter() - start_time
                if elapsed > 0.36:
                    corner_count += 1
                    print(f"🔁 Corner {corner_count}/{max_corners}")
                last_error, integral = 0, 0
                continue
            error = setpoint - d
            integral += error
            derivative = error - last_error
            correction = Kp*error + Ki*integral + Kd*derivative
            servo_angle = 90 + correction
            set_servo_angle(servo_angle)
            start_robot()
            last_error = error
            time.sleep(0.02)
        stop_robot()
        print("🏁 Done 4 corners.")
    except KeyboardInterrupt:
        stop_robot()
    finally:
        servo_pwm.stop()
        motor_pwm.stop()

# ====================
# === LEFT WALL (antik.py)
# ====================
def run_left_wall():
    print("▶▶ Running LEFT wall code...")

    # === GPIO SETUP ===
    TRIG = 25
    ECHO = 8
    SERVO_PIN = 18
    ENA = 22
    IN1 = 17
    IN2 = 27

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    GPIO.setup([ENA, IN1, IN2], GPIO.OUT)

    servo_pwm = GPIO.PWM(SERVO_PIN, 50)
    servo_pwm.start(7.5)
    motor_pwm = GPIO.PWM(ENA, 1000)
    motor_pwm.start(0)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)

    # PID constants
    Kp, Ki, Kd = 6, 0, 0.4
    setpoint = 27
    last_error, integral = 0, 0
    corner_count, max_corners = 0, 12

    def read_distance():
        GPIO.output(TRIG, False)
        time.sleep(0.00001)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        start = time.perf_counter()
        timeout = start + 0.04
        pulse_start, pulse_end = None, None
        while GPIO.input(ECHO) == 0 and time.perf_counter() < timeout:
            pulse_start = time.perf_counter()
        while GPIO.input(ECHO) == 1 and time.perf_counter() < timeout:
            pulse_end = time.perf_counter()
        if pulse_start and pulse_end:
            duration = pulse_end - pulse_start
            distance = round(duration * 17150, 2)
            if distance <= 0: return -1
            if distance > 600: return None
            return distance
        return None

    def set_servo_angle(angle):
        angle = max(60, min(120, angle))
        duty = 2 + ((180 - angle) / 18)  # inverted
        servo_pwm.ChangeDutyCycle(duty)
        print(f"Servo (inv) → {angle:.2f}°")

    def stop_robot():
        motor_pwm.ChangeDutyCycle(0)
        GPIO.output(IN1, False)
        GPIO.output(IN2, False)
        set_servo_angle(90)
        print("🚦 Stopped")

    def start_robot(speed=65):
        motor_pwm.ChangeDutyCycle(speed)
        GPIO.output(IN1, True)
        GPIO.output(IN2, False)
        print(f"🚀 Forward {speed}")

    def approach_wall():
        set_servo_angle(60)
        start_robot(60)
        while True:
            d = read_distance()
            if d and d > 0 and d < 50:
                stop_robot()
                print(f"✅ Found wall {d:.2f}cm")
                break
            time.sleep(0.02)

    try:
        while corner_count < max_corners:
            d = read_distance()
            if d is None: continue
            if d > 60 or d < 0:
                start_time = time.perf_counter()
                stop_robot()
                print(f"⚠️ Wall lost, corner {corner_count+1}")
                approach_wall()
                elapsed = time.perf_counter() - start_time
                if elapsed > 0.6:
                    corner_count += 1
                    print(f"🔁 Corner {corner_count}/{max_corners}")
                last_error, integral = 0, 0
                continue
            error = setpoint - d
            integral += error
            derivative = error - last_error
            correction = Kp*error + Ki*integral + Kd*derivative
            servo_angle = 90 + correction
            set_servo_angle(servo_angle)
            start_robot()
            last_error = error
            time.sleep(0.02)
        stop_robot()
        print("🏁 Done 4 corners.")
    except KeyboardInterrupt:
        stop_robot()
    finally:
        servo_pwm.stop()
        motor_pwm.stop()

# ====================
# === BUTTON LOGIC
# ====================
def wait_for_press_release():
    while GPIO.input(BUTTON_PIN) == 0:
        time.sleep(0.01)
    while GPIO.input(BUTTON_PIN) == 1:
        time.sleep(0.01)
    return True

try:
    wait_for_press_release()  # first press
    print("🔘 First press detected, waiting 2s for possible double press...")
    start = time.time()
    presses = 1

    while time.time() - start < 2:
        if GPIO.input(BUTTON_PIN) == 1:
            wait_for_press_release()
            presses += 1
            break

    if presses == 1:
        run_right_wall()
    elif presses == 2:
        run_left_wall()

finally:
    GPIO.cleanup()
