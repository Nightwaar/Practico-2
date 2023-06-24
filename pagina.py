from flask import render_template
from flask import Flask,request,url_for,redirect,session
import hashlib



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
        return render_template('bienvenida.html')
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
    correo_preceptor = session.get("preceptor")
    preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
    cursos = Curso.query.filter_by(idpreceptor=preceptor.id).all()
    return render_template('cursoclase.html', cursos=cursos, preceptor=preceptor)


@app.route('/asistencia_curso',methods=['POST','GET'])
def asistencia_curso():
    idcurso=request.form.get('cursos')
    curso = Curso.query.filter_by(id=idcurso).first()
    alumnos=Estudiante.query.all()
    return render_template('asistencia_curso.html', curso=curso, alumnos=alumnos)

@app.route('/asistencia_alumno', methods=['GET'])
def asistencia_alumno():
    idcurso = request.args.get('idcurso')
    tipoclase = request.args.get('clase')
    fecha = request.args.get('fecha')
    idalumno = request.args.get('alumno')
    alumno = Estudiante.query.filter_by(id=idalumno).first()
    return render_template('confirmar_asistencia.html', tipoclase=tipoclase, fecha=fecha, alumno=alumno, idcurso=idcurso, idalumno=idalumno)


@app.route('/confirmar_asistencia', methods=['POST'])
def confirmar_asistencia():
    idcurso = request.args.get('idcurso')
    asistencia = Asistencia(fecha=request.form['fecha'], codigoclase=request.form['tipoclase'], asistio=request.form['asis'], justificacion=request.form['justificacion'], idestudiante=request.form.get('idalumno'))
    db.session.add(asistencia)
    db.session.commit()
    cursos=Curso.query.all()
    return redirect(url_for('registrar_asistencia', cursos=cursos))
    
@app.route('/listar_asistencia')
def listar_asistencia():
    correo_preceptor = session.get("preceptor")
    preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
    cursos = Curso.query.filter_by(idpreceptor=preceptor.id).all()
    return render_template('funcionalidad3.html', cursos=cursos, preceptor=preceptor)

@app.route('/informe',methods=['POST','GET'])
def informe():
    idcurso=request.form.get('cursos')
    curso = Curso.query.filter_by(id=idcurso).first()
    alumnos = Estudiante.query.all()
    asistencia=Asistencia.query.all()
    return render_template('listar.html', curso=curso, alumnos=alumnos,asistencia=asistencia)


if __name__=='__main__':
    
    app.run(debug=True)