from spyne import Application, rpc, ServiceBase
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://emre-projet802.pages.dev", "methods": ["GET", "POST", "OPTIONS"], "headers": ["Content-Type"]}})

class TravelTimeService(ServiceBase):
    @rpc(float, float, float, _returns=float, _body_style='wrapped')
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
    elif request.method == 'GET':
        return 'Hello World!'  # Add this line to return 'Hello World!' for GET requests
    else:
        return WsgiApplication(application)

if __name__ == '__main__':
    wsgi_application = WsgiApplication(application)

    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))

    print(f'Listening on {host}:{port}...')

    server = make_server(host, port, app)
    server.serve_forever()
