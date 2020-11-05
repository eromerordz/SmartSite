from BClima import app, mydb
from flask import jsonify, request, render_template
import random
@app.route('/api')
def index():
    y = []
    for x in range(10):
        temp = random.randint(0, 40)
        hum = random.randint(1050, 1150)
        algo = {'Temperatura':temp, 'Humedad':hum}
        y.append(algo)
    return jsonify(y)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/historial')
def historial():
    return render_template('historial.html')

@app.route('/principal')
def principal():
    return render_template('principal.html')

@app.route('/recuperarpsw')
def recuperarpsw():
    return render_template('recuperarpsw.html')
    
@app.route('/recuperarpswH')
def recuperarpswH():
    return render_template('recuperarpswH.html')

@app.route('/sensores')
def sensores():
    return render_template('sensores.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')