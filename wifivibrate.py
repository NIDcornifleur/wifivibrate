import socket
import network
import machine
import utime

ssid = 'PicoW'
password = '**********'

led = machine.Pin("LED", machine.Pin.OUT)
ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

while ap.active() == False:
    pass

print('Connection successful')
print(ap.ifconfig())
led.on()

html = """<!DOCTYPE html>
<html><head>
    <title>Pico W</title>
    <meta http-equiv="refresh" content="5"> <!-- each 5 seconds -->
</head>
<body>
    <h1>RJ</h1>
    <p>Vibration.</p>
    <p>{}</p>
</body>
</html>
"""

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

vibrate = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

def check_vibration():
    if vibrate.value() == 0:
        return True
    else:
        return False

while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)

        vibration = check_vibration()

        if vibration:
            vibration_status = 'Vibration detected'
        else:
            vibration_status = 'No vibration detected'

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html.format(vibration_status))
        cl.close()
        led.off()

        utime.sleep(2)  

    except OSError as e:
        cl.close()
        print('connection closed')

