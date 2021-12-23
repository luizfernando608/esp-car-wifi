#%%
""" PY TO ESP (LED CONTROLLER) """
# Written by Junicchi - https://github.com/Kebablord

# import urllib.request
import requests

# root_url = "http://192.168.0.107"  # ESP's url, ex: http://192.168.102 (Esp prints it to serial console when connected to wifi)

# def sendRequest(url):
# 	n = urllib.request.urlopen(url) # send request to ESP

# Example usage
while True:
	answer = input(""" To control the led, type "ON" or "OFF": """)
	if (answer=="ON"):
		print("ON")
		try:
			requests.get("http://192.168.0.105/CLOSE_LED")
		except:
			pass

	if (answer=="OFF"):
		print("OFF")
		try:
			requests.get("http://192.168.0.105/OPEN_LED")
		except:
			pass
		
		
