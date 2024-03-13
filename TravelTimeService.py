from spyne import Application, rpc, ServiceBase
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class TravelTimeService(ServiceBase):
    @rpc(float, float, float, _returns=float)
    def calculate_travel_time(ctx, distance, autonomy, charging_time):
        return distance / autonomy * charging_time

application = Application([TravelTimeService], 'travel',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

@app.route('/', methods=['POST', 'GET', 'OPTIONS'])
def soap_service():
    if request.method == 'OPTIONS':
        response_headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return '', 200, response_headers
    else:
        return WsgiApplication(application)

if __name__ == '__main__':
    wsgi_application = WsgiApplication(application)

    server = make_server('localhost', 8000, app)
    server.serve_forever()
