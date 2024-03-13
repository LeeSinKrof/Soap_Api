from spyne import Application, rpc, ServiceBase
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
import os



load_dotenv()


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://emre-projet802.pages.dev", "methods": ["POST", "GET", "OPTIONS"], "headers": ["Content-Type"]}})

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
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return '', 200, response_headers
    elif request.method == 'POST':
        response = wsgi_application.__call__(request.environ, response_headers)
        return response
    else:
        return 'Hello World!'


if __name__ == '__main__':
    wsgi_application = WsgiApplication(application)
    app.wsgi_app = wsgi_application

    host = (os.getenv('HOST') or "127.0.0.1")
    port = (int(os.getenv('PORT')) or 8000)

    print(f'Listening on {host}:{port}...')

    server = make_server(host, port, app)
    server.serve_forever()
