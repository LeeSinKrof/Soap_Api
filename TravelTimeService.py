from spyne import Application, rpc, ServiceBase
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": "*", "headers": "*"}})

class TravelTimeService(ServiceBase):
    @rpc(float, float, float, int, _returns=float)
    def calculate_travel_time(ctx, distance, charging_time, max_speed, number_of_stations):
        return (distance / max_speed) + number_of_stations * charging_time

application = Application([TravelTimeService], 'travel',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

@app.route('/', methods=['POST', 'GET', 'OPTIONS'])
def soap_service():
    if request.method == 'OPTIONS':
        response_headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return '', 200, response_headers
    else :
        print('Request received')
        return WsgiApplication(application)


if __name__ == '__main__':
    wsgi_application = WsgiApplication(application)

    host = "0.0.0.0"
    port = 8000


    server = make_server(host, port, app)
    print(f'Listening on {host}:{port}...')

    server.serve_forever()
