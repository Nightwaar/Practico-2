from flask import render_template
from flask import Flask,request,url_for,redirect,session
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
    usuario = Preceptor.query.filter_by(correo=email, clave=clave).first()
    if usuario:
        return redirect(url_for('pagina_preceptor',correo = email))
    else:
        return render_template('inicio.html')

@app.route('/preceptor',methods =['POST','GET'] )
def pagina_preceptor():
    correo = request.args.get('correo')
    session["preceptor"] = correo
    return render_template('paginapreceptor.html')

@app.route('/registrar_asistencia')
def registrar_asistencia():
    cursos=Curso.query.all()
    return render_template('cursoclase.html',cursos=cursos)


@app.route('/asistencia_curso',methods=['POST','GET'])
def asistencia_curso():
    idcurso=request.form['cursos']
    curso=Curso.query.filter_by(id=idcurso).first()
    tipoclase=request.form['clase']
    fecha=request.form['fecha']
    alumnos=Estudiante.query.all()
    return render_template('asistencia_curso.html',curso=curso,tipoclase=tipoclase,fecha=fecha,alumnos=alumnos)

@app.route('/asistencia_alumno',methods=['POST',['GET']])
def asistencia_alumno():
    tipoclase=request.form['clase']
    fecha=request.form['fecha']
    idalumno=request.form.get('alumno')
    return render_template('confirmar_asistencia.html',tipoclase=tipoclase,fecha=fecha,idalumno=idalumno)

@app.route('/listar_asistencia')
def listar_asistencia():
    return render_template('funcionalidad3.html')


if __name__=='__main__':
    
    app.run(debug=True)