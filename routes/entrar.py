from BClima import app, mydb
from flask import Flask,render_template,request,flash,redirect,url_for,session
from flaskext.mysql import MySQL
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

#semilla
# semilla = bcrypt.gensalt()

@app.route("/")

def main():
    if 'nombre' in session:
        return render_template('principal.html')
    else:
        return render_template('home.html')

@app.route('/principal')
def principal():
    if 'nombre' in session:
        return render_template('principal.html')
    else:
        return render_template('home.html')

@app.route('/historial')
def historial():
    if 'nombre' in session:
        return render_template('historial.html')
    else:
        return render_template('home.html')

@app.route('/sensores')
def sensores():
    if 'nombre' in session:
        return render_template('sensores.html')
    else:
        return render_template('home.html')

@app.route('/perfil')
def perfil():
    if 'nombre' in session:
        return render_template('perfil.html')
    else:
        return render_template('home.html')

@app.route('/recuperarpsw')
def recuperarpsw():
    if 'nombre' in session:
        return salir()
    else:
        return render_template('recuperarpsw.html')
    
@app.route('/recuperarpswH')
def recuperarpswH():
    if 'nombre' in session:
        return salir()
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
        # password_encode = password_encode("utf-8")
        cursor = mysql.get_db().cursor()
        # cur = mysql.connection.cursor()

        # sQuery = "SELECT Users_Name, Users_Correo, password_b FROM users WHERE Users_Correo = %s AND password_b = %s"
        # sQuery1 = "SELECT Users_Name, Users_Correo, password_b FROM users WHERE password_b = %s"
        # cursor.execute(sQuery,[correo,passwordB])

        cursor.execute("SELECT * FROM users WHERE Users_Correo = %s AND password_b = %s",(correo,passwordB))
        # cursor.execute(sQuery1,[passwordB])

        usuario = cursor.fetchone()

        cursor.close()

        if (usuario != None):
            # password_encriptado_encode = usuario[2].encode()
            # if (bcrypt.checkpw(password_encode,password_encriptado_encode)):
            # fsw = passwordB
            # if (passwordB == fsw):
            session['id']= usuario[0]
            session['nombre']= usuario[1]
            session['correo']= usuario[2]
            session['pasw']= usuario[3]
            return redirect(url_for('principal'))
            # else:
                # return render_template('home.html')
        else:
            return render_template('home.html')

@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for('entrar'))

