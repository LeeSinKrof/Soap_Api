from spyne import Application, rpc, ServiceBase
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from flask import Flask, request, render_template
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

@app.route('/')
def soap_service():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()