import time
import Adafruit_ADS1x15
from ReadWriteConfig import *

GAIN = 0
with open("PlantMgr.xml","r") as f:
    content = f.read()
    y = BeautifulSoup(content, features = "lxml")
    #print(y)
    print(y.find("gain"))
    GAIN = int(y.find("gain").text)

adc = Adafruit_ADS1x15.ADS1015() # Pick Sensors

print('Reading ADS1x15 values')
# Print nice channel column headers.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)

mSS_Count = 0
mSS_Array = np.full(5, SoilSensors(0, 0.0, 0.0, 0, 0.0))

# seraching for numb. of sensors
for i in range(5):
	values = [0]*4
	for j in range(4):
		values[j] = adc.read_adc(j, gain = GAIN)
	print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
	time.sleep(0.2)
	
for j in range(4):
	if values[j] > 0:
		mSS_Count +=1
		
print("Number of sensors discovered: ", mSS_Count)

for i in range(mSS_Count):
	print("Remove sensor #", i)
	input("Dry sensor and press enter")
	DryVal = adc.read_adc(i, gain = GAIN)
	for j in range(15):
		temp = adc.read_adc(i, gain = GAIN)
		print(temp)
		if temp > DryVal:
			DryVal = temp
		time.sleep(0.5)

	WetVal = adc.read_adc(i, gain = GAIN)
	input("Place sensor in water")
	WetVal = adc.read_adc(i, gain = GAIN)
	for j in range(15):
		temp = adc.read_adc(i, gain = GAIN)
		print(temp)
		if temp < WetVal:
			WetVal = temp	
		time.sleep(0.5)
	a = (100/(DryVal - WetVal))
	b = -1 * a * WetVal
	
	sp = input("Define setpoint for sensor")

	mSS_Array[i] = SoilSensors(i, a, b, 0,sp) 
	
	
print(mSS_Array[0])

print("Values recorded: ", ReadWriteConfig(0, mSS_Array, mSS_Count))
answer = input("Overwrite Conf. Values (y/n): ")
if answer == "y":
	ReadWriteConfig(1, mSS_Array, mSS_Count)
