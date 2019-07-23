import subprocess
import os
import signal
import requests

APIRequestCount = 0
p = subprocess.Popen("pocketsphinx_continuous -inmic yes", stdout=subprocess.PIPE, bufsize=1, shell=True)
for line in iter(p.stdout.readline, b''):
    os.kill(p.pid, signal.SIGTSTP)
    line = str(line.lower())
    line = line[0:len(line)-1]
    if "weather" in line or "whether" in line or "aether" in line or "whethers" in line:
        response = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=37240,us&APPID=10b4269b28392a82dff1ba86e8bc2717').text
        tempStartIndex = response.find("temp")
        kelvin = int(response[tempStartIndex+6:tempStartIndex+9])
        fahrenheit = (kelvin - 273.15) * 1.8 + 32
        print("The temperate is " + str(fahrenheit) + " degrees fahrenheit")
        APIRequestCount += 1
    elif "request" in line or "food" in line or "menu" in line:
        print("Today there is Creamed Corn and more Creamed Corn")
        APIRequestCount += 1
    else:
        print("I'm sorry, I heard " + line)
        APIRequestCount += 1

    if APIRequestCount < 2:
        os.kill(p.pid, signal.SIGCONT)
    else:
        os.kill(p.pid, signal.SIGKILL)

p.stdout.close()
p.wait()

