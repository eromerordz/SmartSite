from clases.sensor import dth22sensor
from BClima import app
from flask import jsonify, request

@app.route('/getsensor')
def getsensor():
    sen = dth22sensor(4)
    temp, hum = sen.readDHT22()
    return jsonify({'temperatura':temp, 'humedad':hum})
