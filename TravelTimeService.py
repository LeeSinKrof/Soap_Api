from spyne import Application, rpc, ServiceBase
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from flask import Flask, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": "*", "headers": "*"}})

class TravelTimeService(ServiceBase):
    @rpc(float, float, int, float, int, _returns=float)
    def calculate_travel_time(ctx, duration, charging_time, number_of_stations, distance_remaining, autonomy):
        proportion_distance_remaining = distance_remaining / autonomy
        remaining_charging_time = proportion_distance_remaining * charging_time
        if number_of_stations == 1:
            return duration + remaining_charging_time
        elif number_of_stations > 1:
            return duration + ((number_of_stations - 1) * charging_time) + remaining_charging_time
        else:
            return duration

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

    host = (os.getenv('HOST') or "0.0.0.0")
    port = (int(os.getenv('PORT')) or 8000)


    server = make_server(host, port, app)
    server.serve_forever()
