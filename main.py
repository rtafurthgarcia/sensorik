import network
from microdot_asyncio import Microdot, send_file
from microdot_asyncio_websocket import with_websocket
from microdot_utemplate import render_template
from machine import UART, Pin, ADC
from camera import TTLCamera
#from onewire import DS18B20, OneWire
import ds18b20
from time import sleep

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(ssid="sensorik_ap", password="trustmebro")

# setup WebServer
app = Microdot()

# setup the camera
#camera = TTLCamera(UART(1, 115200))
#print("Camera connected: v{}".format(camera.getversion()))

# setup the temperature sensor
#ds = DS18B20(OneWire(Pin("PA1")))
#roms = ds.scan()
#if (len(roms) == 0):
#    raise RuntimeError("Couldnt find any temperature sensor!")
#sensor=ds18b20.ds(1,'f',12)

# setup the water lvl sensor 
water_lvl_sensor = ADC(1)

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

# @app.route('/temperature')
# @with_websocket
# async def temperature(request, ws):
#     while True:
#         for rom in roms:
#             #print(ds.read_temp(rom))
#             await ws.send(str(ds18b20.read(sensor)))

@app.route('/liquid-height')
@with_websocket
async def liquid_height(request, ws):
    while True:
        sleep(1)
        water_lvl = water_lvl_sensor.read_u16() / 65535 * 100
        await ws.send(str(water_lvl))

# @app.route('/video-feed')
# @with_websocket
# async def videoFeed(request, ws):
#     while True:
#         camera.takephoto()
#         await ws.send("data:image/jpeg;base64,{}".format(camera.savephototobase64()))

app.run(port=80, host="0.0.0.0", debug=True)