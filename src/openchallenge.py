import RPi.GPIO as GPIO
import time
TRIG = 25
ECHO = 8
ENA = 22  
ENB = 23  
IN1 = 17  
IN2 = 27
IN3 = 24  
IN4 = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup([IN1, IN2, IN3, IN4, ENA, ENB], GPIO.OUT)
left_pwm = GPIO.PWM(ENA, 1000)
right_pwm = GPIO.PWM(ENB, 1000)
left_pwm.start(0)
right_pwm.start(0)
Kp = 30
Kd = 10
Ki = 0
setpoint = 15  # Desired distance from the wall in cm
last_error = 0
integral = 0
def read_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    duration = pulse_end - pulse_start
    distance = duration * 17150
    return round(distance, 2)
def set_motor_speeds(left_speed, right_speed):
    left_speed = max(0, min(100, left_speed))
    right_speed = max(0, min(100, right_speed))

    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)

    left_pwm.ChangeDutyCycle(left_speed)
    right_pwm.ChangeDutyCycle(right_speed)

try:
    base_speed = 50  

    while True:
        distance = read_distance()
        error = setpoint - distance
        integral += error
        derivative = error - last_error

        correction = Kp * error + Ki * integral + Kd * derivative

        left_motor_speed = base_speed - correction
        right_motor_speed = base_speed + correction

        set_motor_speeds(left_motor_speed, right_motor_speed)

        last_error = error
        time.sleep(0.05)

except KeyboardInterrupt:
    GPIO.cleanup()
