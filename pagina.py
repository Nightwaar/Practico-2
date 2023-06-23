from flask import render_template
from flask import Flask,request,url_for,redirect
import hashlib
from flask_login import LoginManager


app=Flask('pagina')
app.config.from_pyfile('config.py')

from modelos import db
from modelos import Curso,Estudiante,Preceptor,Asistencia

@app.route('/')
def bienvenido():
    return render_template('bienvenida.html')

@app.route('/inicio_sesion')
def inicio_sesion():
    return render_template('inicio.html')

@app.route('/verificacion')
def verificacio():
    if request.method =='POST':
        email=request.form['email']
        clave=request.form['contraseña']
        clavecifrada=hashlib.md5(bytes(clave,encoding='utf-8'))
        usuario = Preceptor.query.filtrer_by(email == Preceptor.correo).first()
        
        if usuario and clavecifrada == Preceptor.clave:
            datosform = request.form
            return render_template('paginapreceptor.html',datos=datosform)
        else:
            return render_template('inicio.html')

@app.route('/preceptor',methods= ['POST','GET'])
def pagina_preceptor():
    if request.method =='POST':
        if request.form['correo'] and request.form['contraseña']:
            datosform = request.form
            return render_template('paginapreceptor.html',datos=datosform)
        else:
            return render_template('inicio.html')

@app.route('/registrar_asistencia')
def asistencia():
    return render_template('funcionalidad2.html')



@app.route('/listar_asistencia')
def listar():
    return render_template('funcionalidad3.html')


if __name__=='__main__':
    app.run(debug=True)