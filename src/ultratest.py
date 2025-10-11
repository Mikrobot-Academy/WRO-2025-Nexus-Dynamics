import RPi.GPIO as GPIO
import time

# === Pin setup ===
TRIG = 7
ECHO = 16

GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    # Make sure trigger is low
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    # Send 10us pulse to trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for echo start
    pulse_start = time.time()
    timeout = pulse_start + 0.04  # 40 ms timeout
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None

    # Wait for echo end
    pulse_end = time.time()
    timeout = pulse_end + 0.04
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None

    pulse_duration = pulse_end - pulse_start

    # Distance in cm (speed of sound = 34300 cm/s)
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

try:
    while True:
        dist = measure_distance()
        if dist:
            print(f"Distance: {dist} cm")
        else:
            print("Out of range")
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nMeasurement stopped by User")
    GPIO.cleanup()
