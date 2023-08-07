include("$(BOARD_DIR)/manifest.py")

module("microdot_asgi.py", base_path = "lib/microdot/src")
module("microdot_asgi_websocket.py", base_path = "lib/microdot/src")
module("microdot_asyncio.py", base_path = "lib/microdot/src")
module("microdot_asyncio_test_client.py", base_path = "lib/microdot/src")
module("microdot_asyncio_websocket.py", base_path = "lib/microdot/src")
module("microdot_utemplate.py", base_path = "lib/microdot/src")
module("microdot.py", base_path = "lib/microdot/src")
module("microdot_cors.py", base_path = "lib/microdot/src")
module("microdot_session.py", base_path = "lib/microdot/src")
module("microdot_ssl.py", base_path = "lib/microdot/src")
module("microdot_websocket_alt.py", base_path = "lib/microdot/src")
module("microdot_websocket.py", base_path = "lib/microdot/src")
module("microdot_wsgi.py", base_path = "lib/microdot/src")

module("compiled.py", base_path="lib/utemplate/utemplate")
module("recompile.py", base_path="lib/utemplate/utemplate")
module("source.py", base_path="lib/utemplate/utemplate")

package("utemplate", base_path="lib/utemplate")

module("camera.py")