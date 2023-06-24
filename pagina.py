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

@app.route('/verificacion',methods= ['POST','GET'])
def verificacion():
    email=request.form['correo']
    clave=request.form['contrasena']
    if not email and not clave:
        return redirect(url_for("templates",filename='inicio.html'))
    # clavecifrada=hashlib.md5(bytes(clave,encoding='utf-8')).digest()
    usuario = Preceptor.query.filter_by(correo=email, clave=clave).first()
    if usuario:
        datosform = request.form
        return render_template('paginapreceptor.html',datos=datosform)
    else:
        return render_template('datos.html',usuario=usuario)

@app.route('/preceptor')
def pagina_preceptor():
    preceptores=Preceptor.query.all()
    return render_template('paginapreceptor.html',preceptores=preceptores)

@app.route('/registrar_asistencia')
def registrar_asistencia():
    return render_template('funcionalidad2.html')



@app.route('/listar_asistencia')
def listar_asistencia():
    return render_template('funcionalidad3.html')


if __name__=='__main__':
    
    app.run(debug=True)