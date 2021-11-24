# PlantManager

Automatic plant watering scripts for a Raspberry Pi Zero 2 W.

**Calibration.py** checks for any soil sensors that are plugged in and walks the user through the steps to perform a calibration of the sensors in dry air then in water.  Calibration values are saved in an xml config file.\
\
**ReadWriteConfig.py** is used to read/write sensor settings from the xml calibration file.\
\
**CheckWater.py** sets up the motors, sensors, reads calibration values, and sets up an indicator LED.  Motors are ran once to indicate the script is running.  The script then checks the soil sensors, compares against the calibration and setpoint values saved in the config.  The motors are then ran several times until the soil sensors read appropriate water levels.

![image](https://user-images.githubusercontent.com/51388454/143171611-f7d5be5b-6044-45bc-9d46-585121e6fb46.png)
