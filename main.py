import network
from microdot import Microdot

ap = network.WLAN(network.AP_IF)
ap.config(ssid="lmao_wtf_dd", password="trustmebro")
ap.active(True)

app = Microdot()

@app.route('/')
def index(request):
    return 'Hello, world!'

app.run(port=80, host="0.0.0.0", debug=True)