from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template_string
from flask_sockets import Sockets
import json

app = Flask(__name__)
sockets = Sockets(app)

template = """
<html><body><table>
{% for key, value in appliances.items() %}
<tr><td>{{ key }}</td><td>{{ value }}</td></tr>
{% endfor %}
</table>
<form>
<input type="text" id="device">
<input type="number" id="capacity" step="1" pattern="\d*">
<input type="submit">
</form>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
<script type="text/javascript">
$(function() {
  var socket = new WebSocket("ws://" + document.domain + ":5000/api");
  socket.onmessage = function(message) {
    var data = JSON.parse(message.data);
    $("table").append("<tr><td>" + data.device + "</td><td>" + data.capacity + "</td></tr>");
  };
  $("form").submit(function(event) {
    var data = {"device" : $("#device").val(), "capacity" : parseInt($("#capacity").val(), 10)};
    socket.send(JSON.stringify(data));
    event.preventDefault();
  });
});
</script>
</body></html>
"""


@app.route('/')
def index():
    with open('appliances.json', 'r') as json_file:
        appliances = json.load(json_file)
    return render_template_string(template, appliances=appliances)


@sockets.route('/api')
def api(socket):
    while True:
        message = socket.receive()
        socket.send(message)
        data = json.loads(message)
        with open('appliances.json', 'r') as json_file:
            appliances = json.load(json_file)
        appliances[data['device']] = data['capacity']
        with open('appliances.json', 'w') as json_file:
            json.dump(appliances, json_file)


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()


# import base64
# import json
# import logging
#
# from flask import Flask
# from flask_sockets import Sockets
# from flask import Flask, request, render_template_string
#
# app = Flask(__name__)
# sockets = Sockets(app)
#
# HTTP_SERVER_PORT = 5000
#
# template = """
# <html><body><table>
# {% for key, value in appliances.iteritems() %}
# <tr><td>{{ key }}</td><td>{{ value }}</td></tr>
# {% endfor %}
# </table>
# <form>
# <input type="text" id="device">
# <input type="number" id="capacity" step="1" pattern="\d*">
# <input type="submit">
# </form>
# <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
# <script type="text/javascript">
# $(function() {
#   var socket = new WebSocket("ws://" + document.domain + ":5000/api");
#   socket.onmessage = function(message) {
#     var data = JSON.parse(message.data);
#     $("table").append("<tr><td>" + data.device + "</td><td>" + data.capacity + "</td></tr>");
#   };
#   $("form").submit(function(event) {
#     var data = {"device" : $("#device").val(), "capacity" : parseInt($("#capacity").val(), 10)};
#     socket.send(JSON.stringify(data));
#     event.preventDefault();
#   });
# });
# </script>
# </body></html>
# """
#
# @app.route('/')
# def index():
#     with open('appliances.json', 'r') as json_file:
#         appliances = json.load(json_file)
#     return render_template_string(template, appliances=appliances)
#
#
# @sockets.route('/media')
# def echo(ws):
#     app.logger.info("Connection accepted")
#     # A lot of messages will be sent rapidly. We'll stop showing after the first one.
#     has_seen_media = False
#     message_count = 0
#     while not ws.closed:
#         message = ws.receive()
#         if message is None:
#             app.logger.info("No message received...")
#             continue
#
#         # Messages are a JSON encoded string
#         data = json.loads(message)
#
#         # Using the event type you can determine what type of message you are receiving
#         if data['event'] == "connected":
#             app.logger.info("Connected Message received: {}".format(message))
#         if data['event'] == "start":
#             app.logger.info("Start Message received: {}".format(message))
#         if data['event'] == "media":
#             if not has_seen_media:
#                 app.logger.info("Media message: {}".format(message))
#                 payload = data['media']['payload']
#                 app.logger.info("Payload is: {}".format(payload))
#                 chunk = base64.b64decode(payload)
#                 app.logger.info("That's {} bytes".format(len(chunk)))
#                 app.logger.info("Additional media messages from WebSocket are being suppressed....")
#                 has_seen_media = True
#         if data['event'] == "closed":
#             app.logger.info("Closed Message received: {}".format(message))
#             break
#         message_count += 1
#
#     app.logger.info("Connection closed. Received a total of {} messages".format(message_count))
#
#
# if __name__ == '__main__':
#     app.logger.setLevel(logging.DEBUG)
#     from gevent import pywsgi
#     from geventwebsocket.handler import WebSocketHandler
#
#     server = pywsgi.WSGIServer(('', HTTP_SERVER_PORT), app, handler_class=WebSocketHandler)
#     print("Server listening on: http://localhost:" + str(HTTP_SERVER_PORT))
#     server.serve_forever()



# from flask import Flask
# from flask_sockets import Sockets
# import logging
# from gevent import pywsgi
# from geventwebsocket.handler import  WebSocketHandler
# import json
# import base64
#
# app = Flask(__name__)
# sockets = Sockets(app)
#
# HTTP_SERVER_PORT = 5005
#
#
# @sockets.route('/media')
# def echo(ws):
#     app.logger.info("Connection Accepted!")
#     has_seen_media = False
#     message_count = 0
#
#     while not ws.closed:
#         message = ws.received()
#         if message is None:
#             app.logger.info("No message received...")
#             continue
#
#         data = json.load(message)
#
#         if data['event'] == 'connected':
#             app.logger.info("Connected Message received: {}".format(message))
#         if data['event'] == 'start':
#             app.logger.info("Start message received: {}".format(message))
#         if data['event'] == 'media':
#             if not has_seen_media:
#                 app.logger.info("Media message: {}".format(message))
#                 payload = data['media']['payload']
#                 app.logger.info("Payload is: {}".format(payload))
#                 chunk = base64.b64decode(payload)
#                 app.logger.info("That's {} bytes".format(len(chunk)))
#                 app.logger.info("Additional media messages from the websocket are being suppressed...")
#                 has_seen_media = True
#         if data['event'] == 'closed':
#             app.logger.info("Closed message received: {}".format(message))
#             break
#     app.logger.info("Connection Closed. Received a total of {} message".format(message_count))
#
#
# if __name__ == '__main__':
#     app.logger.setLevel(logging.DEBUG)
#
#     server = pywsgi.WSGIServer(('', HTTP_SERVER_PORT), app, handler_class=WebSocketHandler)
#     print("Server listening on: http://localhost:" + str(HTTP_SERVER_PORT))
#     server.serve_forever()