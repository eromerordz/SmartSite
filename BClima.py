from flask import Flask, escape, request
from flask_cors import CORS
import decimal
import flask.json
import os
#import flask_login import LoginManager
#from clases.model_login.py import users


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
    "user":"rasp",
    "password":"cactus",
    "database":"rasp_web",
    "auth_plugin":'mysql_native_password'
}
app.config['SECRET_KEY']="FabricaSoftware$FIME$2020"
#login_manager = LoginManager(app)

#@login_manager.user_loader
#def load_user(user_id):
#    for user in users:
#        if(user.id == int(user_id)):
#            return user
#    return None
app.json_encoder = MyJSONEncoder

from routes.route import *
from routes.login import *
from routes.sensor import *


if __name__=="__main__":
    app.debug = True
    host = os.environ.get('IP','127.0.0.1')
    port = int(os.environ.get('PORT',5000))
    app.run(host = host, port=port)
