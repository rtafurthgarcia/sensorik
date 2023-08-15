import network
from microdot_asyncio import Microdot, send_file
from microdot_asyncio_websocket import with_websocket
from microdot_utemplate import render_template
from machine import UART, Pin, ADC
import onewire 
#from vc0706 import VC0706
#from onewire import DS18B20, OneWire
import ds18x20
try:
    import auth
except:
    print("Please add an auth.py file to set both the SSID and the PASS for your access point")
    exit(2)
from math import trunc
from time import sleep, sleep_ms

ap = network.WLAN(network.AP_IF)
# gotta shut it down first otherwise settings will never be applied
ap.active(False) 
ap.config(ssid=auth.SSID, security=2, key=auth.PASS)
ap.active(True)

# setup WebServer
app = Microdot()

# setup the camera
#camera = VC0706(115200, 100)
#print(camera.version)
#print("Camera connected: v{}".format(camera.getversion()))

# setup the temperature sensor
#ds = DS18B20(OneWire(Pin("PA1")))
#roms = ds.scan()¨
#if (len(roms) == 0):
#    raise RuntimeError("Couldnt find any temperature sensor!")
#sensor=ds18b20.ds(1,'f',12)

# setup the water lvl sensor 
water_lvl_sensor = ADC(0)

# setup the temperature sensor 
temperature_sensor = ds18x20.DS18X20(onewire.OneWire(Pin(Pin.board.PH15))) 
temperature_outputs = temperature_sensor.scan()  

# PA9 / PA10 -> Kamera
# PA1-> Flüssigkeitsensor
# PA4  -> Temperature

@app.route('/')
async def index(request):
    return render_template("index.html", title="title lmao"), {'Content-Type': 'text/html'}

@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path, max_age=86400)

@app.route('/temperature')
@with_websocket
async def temperature(request, ws):
    while True:
        temperature_sensor.convert_temp()
        sleep_ms(750)
        for output in temperature_outputs:
            temperature = trunc(temperature_sensor.read_temp(output))
            print("temperature is at: " + str(temperature))
            await ws.send(str(temperature))

@app.route('/liquid-height')
@with_websocket
async def liquid_height(request, ws):
    while True:
        sleep(1)
        water_lvl = trunc(water_lvl_sensor.read_u16() / 65535 * 100)
        print("water level is at: " + str(water_lvl))
        await ws.send(str(water_lvl))

@app.route('/video-feed')
@with_websocket
async def videoFeed(request, ws):
    while True:
        camera.takephoto()
        await ws.send("data:image/jpeg;base64,{}".format(camera.savephototobase64()))

app.run(port=80, host="0.0.0.0", debug=True)