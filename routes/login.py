from BClima import app, mydb
from flask import jsonify, request, render_template, session
import mysql.connector
import bcrypt

@app.route('/login')
def login():
    return render_template('hello.html')

@app.route('/okey')
def okey():
    if session['clima'] == app.config['SECRET_KEY']:
        return render_template('hello.html')
    else:
        return jsonify(False)

@app.route("/postRegistro", methods=["POST","GET"])
def postRegistro():
    data = request.form.to_dict()
    email = data['email'] 
    name = data['name']
    passw = str(data['pass'])+','+str(data['email'])
    passw = hapassword(passw.encode('utf-8')).decode('utf-8')
    try:
        cnx = mysql.connector.connect(**mydb)
        cur = cnx.cursor()
        cur1 = cnx.cursor(buffered=True)
        try:
            query1 = "SELECT COUNT('x') FROM Users WHERE Users_Correo = '%s';"%(email)
            cur1.execute(query1)
            result = [x for x in cur1][0][0]
            if result < 1 :
                query = "INSERT INTO Users (Users_Name,Users_Correo,password_b) VALUES ('%s', '%s', '%s');"%(name, email, passw)
                cur.execute(query)
                cnx.commit()
                return jsonify({'msg':str(data)})
            else:
                return jsonify({'msg':'ERROR:Ya existe este correo registrado'})
        except Exception as e:
            return jsonify({'msg':'ERROR:'+str(e)})
        finally:
            cur1.close()
            cur.close()
            cnx.close()
    except Exception as e:
        return jsonify({'msg':str(e)})

@app.route("/getRegistro", methods=["POST","GET"])
def getRegistro():
    data = request.args.to_dict()
    email = data['email']
    contra = data['pass']
    try:
        cnx = mysql.connector.connect(**mydb)
        cur = cnx.cursor(buffered=True)
        arr = []
        nombres = ["Id","Nombre", "Correo", "Password"]
        try:
            cur.execute("SELECT users_id, users_name, users_correo, password_b FROM Users WHERE Users_Correo="+email+";")
            result = [dict(zip(nombres,x)) for x in cur]
            contra = hapassword(contra.encode('utf-8'), result[0]['Password'])
            if contra:
                session['clima'] = app.config['SECRET_KEY']
                return jsonify(True)
            else:
                return jsonify(False)
        except Exception as e:
            return jsonify({'msg':'ERROR:'+str(e)})
        finally:
            cur.close()
            cnx.close()
    except Exception as e:
        return jsonify({'msg':str(e)})

def hapassword(password_orig, password_h=None):
    if(password_h == None):
        hashed = bcrypt.hashpw(password_orig, bcrypt.gensalt())
        return hashed
    else:
        conf = bcrypt.checkpw(password_orig, password_h)
        return conf