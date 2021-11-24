from bs4 import BeautifulSoup
import numpy as np

class SoilSensors:
	def __init__(self, index, a, b, onHours, setpoint):
		self.index = index
		self.a = a
		self.b = b
		self.onHours = onHours
		self.setpoint = setpoint

oSS_Array =[]

def ReadWriteConfig(write, iSS_Array, iSS_Count):
	with open("PlantMgr.xml", "r") as f:
		content = f.read()
		y = BeautifulSoup(content, features = "lxml")
		oSS_Count = int(y.find("ss_count").text)

		SS_datas = y.find_all("ss")

		for SS_data in SS_datas:
			i = int(SS_data.ssid.text)
			if i <= iSS_Count-1:
				
				oSS_Array.append(SoilSensors(i,
						float(SS_data.a.text),
						float(SS_data.b.text),
						int(SS_data.onhours.text),
						float(SS_data.setpoint.text)))
				if write:
					SS_data.ssid.string = str(iSS_Array[i].index)
					SS_data.a.string = str(iSS_Array[i].a)
					SS_data.b.string = str(iSS_Array[i].b)
					SS_data.onhours.string = str(iSS_Array[i].onHours)
					SS_data.setpoint.string = str(iSS_Array[i].setpoint)
		if write:
			y.find("ss_count").string = str(iSS_Count)
			print(y)
			k = open("PlantMgr.xml", "w")
			k.write(y.prettify())
			k.close()
	#print(oSS_Array)
	#print(oSS_Array[0].a)
	return oSS_Array


