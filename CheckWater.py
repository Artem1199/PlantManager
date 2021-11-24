import RPi.GPIO as GPIO
import time
from ReadWriteConfig import *
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1015() # Pick Sensors

GAIN = 0  #import gain for adc reading
SS_COUNT = 0
with open("PlantMgr.xml", "r") as f:
    content = f.read()
    y = BeautifulSoup(content, features = "lxml")
    #print(y)
    print(y.find("gain"))
    GAIN = int(y.find("gain").text)
    SS_COUNT = int(y.find("ss_count").text)

mSS_Array = np.full(5, SoilSensors(0,0.0, 0.0,0, 0.0))
SS_ARRAY = ReadWriteConfig(0, mSS_Array, SS_COUNT)

print(SS_ARRAY)

PWM0Pin = 18
PWM1Pin = 12
LED0Pin	= 14

# pwm0 setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM0Pin, GPIO.OUT)
GPIO.output(PWM0Pin, GPIO.LOW)
pwm0 = GPIO.PWM(PWM0Pin, 30000)

# pwm1 setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM1Pin, GPIO.OUT)
GPIO.output(PWM1Pin, GPIO.LOW)
pwm1 = GPIO.PWM(PWM1Pin, 30000)

pwm_array = [pwm0, pwm1]

GPIO.setup(LED0Pin, GPIO.OUT)
GPIO.output(LED0Pin, GPIO.HIGH)





for item in SS_ARRAY:
	print("index: ", item.index)
	print("Setpoint: ", item.setpoint)
	print("Cal Value: ", item.a)
	print("b value: ", item.b)
	#SensorVal = adc.read_adc(item.index, gain = GAIN)
	SensorVal = 0
	for _ in range(5):
		SensorVal += adc.read_adc(item.index, gain = GAIN)
		time.sleep(0.1)
	SensorVal = SensorVal / 5 
	print("Sensor reading: ", SensorVal)
	a = item.a
	b = item.b
	setpoint = item.setpoint
	print("Sensor * cal + b: ", SensorVal * a + b)

	# run at low power to indicate running
	pwm_array[item.index].start(10)
	time.sleep(0.2)
	pwm_array[item.index].stop(0)

	overflowCounter = 0
	while((SensorVal * a + b) > setpoint):
		if overflowCounter > 15:
			print("Reached overflow counter")
			break
		# check for wire open on sensor
		if SensorVal < 1200:
			# Run motors
			pwm_array[item.index].start(100)
			time.sleep(2)
			pwm_array[item.index].stop(0)

			overflowCounter += 1
			SensorVal = 0

			# Read new sensor values
			for _ in range(5):
				SensorVal += adc.read_adc(item.index, gain = GAIN)
				time.sleep(0.1)

			SensorVal = SensorVal / 5 
			print("Sensor val measurement loop: ", SensorVal * a + b)
		else:
			print("Check sensor connection.")
			break

	pwm_array[item.index].stop(0)

# hold LED on after completion
time.sleep(10)
GPIO.output(LED0Pin, GPIO.LOW)