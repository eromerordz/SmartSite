#from clases.sensor import dth22sensor
from BClima import app, mydb
from flask import jsonify, request, render_template, session ,redirect, url_for, flash
import random
import mysql.connector

@app.route('/getsensor')
def getsensores():
    sen = dth22sensor(4)
    temp, hum = sen.readDHT22()
    return jsonify({'temperatura':temp, 'humedad':hum})

@app.route('/postsensores', methods=["POST"])
def postsensor():
    data = request.form.to_dict()
    nombre = data['name'] 
    pin = data['pin']
    tipo = data['tipo']
    print(data)
    try:
        cnx = mysql.connector.connect(**mydb)
        cur = cnx.cursor()
        cur1 = cnx.cursor(buffered=True)
        try:
            query1 = "SELECT COUNT('x') FROM sensor WHERE pin = '%s';"%(pin)
            cur1.execute(query1)
            result = [x for x in cur1][0][0]
            if result < 1 :
                query = "INSERT INTO sensor (Nombre, Pin, Tipo) VALUES ('%s', %s, %s);"%(nombre, pin, tipo)
                cur.execute(query)
                cnx.commit()
                flash("Sensor agregado","success")
                return redirect(url_for('sensores'))
            else:
                return jsonify({'msg':'ERROR:Ya existe este sensor registrado'})
        except Exception as e:
            return jsonify({'msg':'ERROR:'+str(e)})
        finally:
            cur1.close()
            cur.close()
            cnx.close()
    except Exception as e:
        return jsonify({'msg':str(e)})

@app.route("/getsensores", methods=["POST","GET"])
def getallsensores():
    try:
        cnx = mysql.connector.connect(**mydb)
        cur = cnx.cursor(buffered=True)
        arr = []
        nombres = ["Id","Nombre", "Pin", "Tipo"]
        try:
            cur.execute("SELECT * FROM sensor;")
            result = [dict(zip(nombres,x)) for x in cur]
            return jsonify(result)
        except Exception as e:
            return jsonify({'msg':'ERROR:'+str(e)})
        finally:
            cur.close()
            cnx.close()
    except Exception as e:
        return jsonify({'msg':str(e)})

@app.route('/putsensores')
def putsensor():
    data = request.form.to_dict()
    index = data['id']
    nombre = data['name'] 
    pin = data['pin']
    tipo = data['type']
    try:
        cnx = mysql.connector.connect(**mydb)
        cur = cnx.cursor()
        try:
            query = "UPDATE sensor SET Nombre ='%s', Pin = %d, Tipo = %d WHERE Id = %d;"%(nombre, tipo, pin, index)
            cur.execute(query)
            cnx.commit()
            return jsonify([x for x in cur][0][0])
        except Exception as e:
            return jsonify({'msg':'ERROR:'+str(e)})
        finally:
            cur.close()
            cnx.close()
    except Exception as e:
        return jsonify({'msg':str(e)})

@app.route("/edit/<id>")
def editSensor(id):
    cnx = mysql.connector.connect(**mydb)
    cur = cnx.cursor()
    cur.execute("SELECT * FROM sensor WHERE Id={0}".format(id))
    data = cur.fetchall()
    return render_template('editsensor.html', sens = data[0])
    
@app.route("/updateSensor/<id>", methods=['POST'])
def updateSensor(id):
    if (request.method == 'POST'):
        name = request.form['name']
        tipo = request.form['tipo']
        pin = request.form['pin']
        cnx = mysql.connector.connect(**mydb)
        cur = cnx.cursor()
        cur.execute("""
        UPDATE sensor
        SET Nombre = %s,
        Tipo = %s,
        Pin = %s
        WHERE Id = %s
        """, (name,tipo,pin,id))
        cnx.commit()
        flash("Sensor actualizado","warning")
        return redirect(url_for('sensores'))
       
@app.route("/delete/<string:id>")
def deleteSensor(id):
    cnx = mysql.connector.connect(**mydb)
    cur = cnx.cursor()
    cur.execute("DELETE FROM sensor WHERE Id={0}".format(id))
    cnx.commit()
    flash("Sensor eliminado","danger")
    return redirect(url_for('sensores'))

@app.route('/getexemplotemphum')
def getexample():
    r1 = random.random()
    r2 = random.random()
    temp = distribucion_normal(r1)
    hum = distribucion_normal(r2)
    return jsonify({'temperatura':temp, 'humedad':hum})

@app.route('/gethoratemphum')
def gethoratemphum():
    try:
        cnx = mysql.connector.connect(**mydb)
        cur = cnx.cursor(buffered=True)
        arr = []
        result = []
        nombres = ["sensor", "temp", "humedad", "hora"]
        try:
            cur.callproc('promedio_24h')
            for x in cur.stored_results():
                hora = [dict(zip(nombres,y)) for y in x]
                result.append(hora)
            return jsonify(result)
            print(result)
        except Exception as e:
            return jsonify({'msg':'ERROR:'+str(e)})
        finally:
            cur.close()
            cnx.close()
    except Exception as e:
        return jsonify({'msg':str(e)})



