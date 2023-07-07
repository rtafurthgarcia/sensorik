import network
from microdot_asyncio import Microdot, send_file
from microdot_asyncio_websocket import with_websocket
from microdot_utemplate import render_template
import random

ap = network.WLAN(network.AP_IF)
ap.config(ssid="lmao_wtf_dd", key="trustmebro")
ap.active(True)

app = Microdot()

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
def temperature(request, ws):
    while True:
        ws.send(random.randrange(20,25))

@app.route('/liquid-height')
@with_websocket
def liquid_height(request, ws):
    while True:
        ws.send(random.randrange(20,25))

@app.route('/video-feed')
@with_websocket
def videoFeed(request, ws):
    while True:
        ws.send("lmao")


app.run(port=80, host="0.0.0.0", debug=True)