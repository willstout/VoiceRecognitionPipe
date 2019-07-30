import subprocess
import os
import signal
import requests
import time

APIRequestCount = 0
writeMode = False
p = subprocess.Popen("pocketsphinx_continuous -inmic yes", stdout=subprocess.PIPE, bufsize=1, shell=True)

for line in iter(p.stdout.readline, b''):
    os.kill(p.pid, signal.SIGTSTP)
    line = str(line.lower())
    line = line[0:len(line)-1]
    if writeMode:
        if "close" in line:
            APIRequestCount += 1
            writeMode = False
        else:
            f = open("patient_info.txt","w+")
            f.write(line)
            f.close() 
    else:
        if "patient" in line and "documentation" in line:
            os.system("open patient_docs.jpg")
            APIRequestCount += 1
            writeMode = False
        elif "write" in line:
            APIRequestCount += 1
            writeMode = True
        elif "name" in line and "nurse" in line:
            print("The name of your nurse is Jane Doe")
            APIRequestCount += 1
            writeMode = False
        elif "weather" in line or "whether" in line:
            response = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=37240,us&APPID=10b4269b28392a82dff1ba86e8bc2717').text
            tempStartIndex = response.find("temp")
            kelvin = int(response[tempStartIndex+6:tempStartIndex+9])
            fahrenheit = (kelvin - 273.15) * 1.8 + 32
            print("The temperate is " + str(fahrenheit) + " degrees fahrenheit")
            APIRequestCount += 1
            writeMode = False
        elif "timer" in line:
            time.sleep(3)
            print("Timer done")
            APIRequestCount += 1
            writeMode = False
        else:
            print("Sorry I didn't quite catch that")

    if APIRequestCount < 1:
        os.kill(p.pid, signal.SIGCONT)
    else:
        os.kill(p.pid, signal.SIGKILL)

p.stdout.close()
p.wait()

