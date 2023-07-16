import network
from microdot_asyncio import Microdot, send_file
from microdot_asyncio_websocket import with_websocket
from microdot_utemplate import render_template
from machine import UART
from camera import TTLCamera

import random

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(ssid="sensorik_ap", password="trustmebro")

# setup WebServer
app = Microdot()

camera = TTLCamera(UART(1, 115200))

# PA9 / PA10 -> Kamera
# PA0 -> Flüssigkeitsensor
# PA4 -> Temperature

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
        await ws.send(str(random.randrange(150,160)))

@app.route('/liquid-height')
@with_websocket
async def liquid_height(request, ws):
    while True:
        await ws.send(str(random.randrange(110,150)))

@app.route('/video-feed')
@with_websocket
async def videoFeed(request, ws):
    while True:
        camera.takephoto()
        await ws.send("data:image/jpeg;base64,{}".format(camera.savephototobase64()))

app.run(port=80, host="0.0.0.0", debug=True)