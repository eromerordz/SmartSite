from BClima import app, mydb
from flask import Flask,render_template,request,flash,redirect,url_for,session
from flaskext.mysql import MySQL
from flask import jsonify
import pymysql 
import re
import bcrypt

app.secret_key="smartsite"

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'leonnegro10'
app.config['MYSQL_DATABASE_DB'] = 'rasp_web'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()

cursor = conn.cursor(pymysql.cursors.DictCursor)

@app.route("/")

def main():
    if 'nombre' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM datosth ORDER BY ID DESC LIMIT 1")
        data = cursor.fetchall()
        return render_template('principal.html', actual = data)
    else:
        return render_template('home.html')

@app.route('/principal')
def principal():
    if 'nombre' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM datosth ORDER BY ID DESC LIMIT 1")
        data = cursor.fetchall()
        return render_template('principal.html', actual = data)
    else:
        return render_template('login.html')

@app.route('/enter')
def enter():
    if 'nombre' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM datosth ORDER BY ID DESC LIMIT 1")
        data = cursor.fetchall()
        return render_template('principal.html', actual = data)    
    else:
        return render_template('login.html')

@app.route('/historial')
def historial():
    if 'nombre' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM datosth ORDER BY ID DESC")
        data = cursor.fetchall()
        return render_template('historial.html', history = data)
    else:
        return render_template('login.html')

@app.route('/sensores')
def sensores():
    if 'nombre' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM sensor")
        data = cursor.fetchall()
        return render_template('sensores.html', sens = data)
    else:
        return render_template('login.html')

@app.route('/perfil')
def perfil():
    if 'nombre' in session:
        return render_template('perfil.html')
    else:
        return render_template('login.html')

@app.route('/cambiar')
def cambiar():
    if 'nombre' in session:
        return render_template('cambiarpsw.html')
    else:
        return render_template('login.html')

@app.route('/p')
def p():
    if 'nombreC' in session:
        return render_template('recuperarpsw.html')
    else:
        return render_template('recuperarpswH.html')

@app.route('/entrar',methods=['GET','POST'])
def entrar():
    if (request.method=='GET'):
        if 'nombre' in session:
            return render_template('principal.html')
        else:
            return render_template('home.html')
    else:
        correo = request.form["nmCorreo"]
        passwordB = request.form["nmPassword"]
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM users WHERE Users_Correo = %s AND password_b = %s",(correo,passwordB))
        usuario = cursor.fetchone()
        cursor.close()
        if (usuario != None):
            session['id']= usuario[0]
            session['nombre']= usuario[1]
            session['correo']= usuario[2]
            session['pasw']= usuario[3].decode("utf-8")
            return redirect(url_for('principal'))
        else:
            flash("Usuario Incorrecto","danger")
            return render_template('login.html')

@app.route('/rpC')
def rpC():
    if 'nombre' in session:
        return redirect(url_for('enter'))
    else:
        return render_template('recuperarpswH.html')   

@app.route('/recuperarpswH', methods=['GET','POST'])
def recuperarpswH():
    if (request.method=='POST'):
        if 'nombre' in session:
            return salir()           
        else:
            correor = request.form["correo"]
            cursor = mysql.get_db().cursor()
            cursor.execute("SELECT * FROM users WHERE Users_Correo = %s",(correor))
            usuario2 = cursor.fetchone()
            cursor.close()
            if (usuario2 != None):
                session['idC']= usuario2[0]
                session['nombreC']= usuario2[1]
                session['correoC']= usuario2[2]
                session['paswC']= usuario2[3].decode("utf-8")
                return render_template('recuperarpsw.html')
            else:
                flash("Correo Incorrecto","danger")
                return render_template('recuperarpswH.html')                
    else:
        return salir() 

@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for('entrar'))
