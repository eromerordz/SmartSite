from flask import Flask, escape, request
from flask_cors import CORS
import decimal
import flask.json
import os
import threading
import time
from clases.sensor import *

class MyJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            #Convierte instancias decimales en strings
            return int(obj)
        return super(MyJSONEncoder, self).default(obj)

app = Flask(__name__)
CORS(app)
mydb = {
    "host":"localhost",
    "user":"root",
    "password":"leonnegro10",
    "database":"rasp_web",
    "auth_plugin":'mysql_native_password'
}
app.config['SECRET_KEY']="FabricaSoftware$FIME$2020"
app.json_encoder = MyJSONEncoder

from routes.route import *
from routes.login import *
from routes.sensor import *
from routes.entrar import *


if __name__=="__main__":
    t1 = threading.Thread(target = asincTemHum)
    t1.start()
    app.debug = True
    host = os.environ.get('IP','127.0.0.1')
    port = int(os.environ.get('PORT',5000))
    app.run(host = host, port=port)