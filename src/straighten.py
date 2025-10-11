import RPi.GPIO as GPIO
import time

SERVO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz for servo
pwm.start(0)

def set_angle(angle):
    # Clamp angle between 0 and 180
    angle = max(0, min(180, angle))
    duty = 2.5 + (angle / 180.0) * 10  # Map 0–180° to 2.5–12.5 duty cycle
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # give servo time to move
    pwm.ChangeDutyCycle(0)  # stop signal to avoid jitter

try:
    print("Setting servo to straight (90°)...")
    set_angle(90)
    input("Press Enter to quit...")

finally:
    pwm.stop()
    GPIO.cleanup()
