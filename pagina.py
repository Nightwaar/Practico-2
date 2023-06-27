from flask import render_template
from flask import Flask,request,url_for,redirect,session,flash
from datetime import *
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
    clavecifrada=hashlib.md5(clave.encode()).hexdigest()
    if not email and not clave:
        return render_template('bienvenida.html')
    usuario = Preceptor.query.filter_by(correo=email, clave=clavecifrada).first()
    if usuario:
        session["preceptor"] = email
        return redirect(url_for('pagina_preceptor',correo = email))
    else:
        flash('Correo o contraseña incorrectos', 'error')
        return render_template('inicio.html')

@app.route('/preceptor',methods =['POST','GET'] )
def pagina_preceptor():
    email = request.form.get('correo')
    correo_preceptor = session.get("preceptor")
    usuario = Preceptor.query.filter_by(correo=correo_preceptor).first()
    return render_template('paginapreceptor.html',correo=correo_preceptor, nombre=usuario.nombre, apellido=usuario.apellido)

# @app.route('/registrar_asistencia')
# def registrar_asistencia():
#     correo_preceptor = session.get("preceptor")
#     preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
#     cursos = Curso.query.filter_by(idpreceptor=preceptor.id).all()
#     return render_template('cursoclase.html', cursos=cursos, preceptor=preceptor)


# @app.route('/asistencia_curso',methods=['POST','GET'])
# def asistencia_curso():
#     idpreceptor=request.args.get('idpreceptor')
#     correo_preceptor = session.get("preceptor")
#     fecha = request.args.get('fecha')
#     codigoclase = request.args.get('tipoclase') 
#     preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
#     idcurso=request.form.get('cursos')
#     curso = Curso.query.filter_by(id=idcurso).first()
#     alumnos=Estudiante.query.all()
#     return render_template('asistencia_curso.html', curso=curso,fecha=fecha,codigoclase=codigoclase, alumnos=alumnos,preceptor=preceptor)

# @app.route('/asistencia_alumno', methods=['GET'])
# def asistencia_alumno():
#     fecha = request.args.get('fecha')
#     codigoclase = request.args.get('tipoclase') 
#     idcurso = request.args.get('idcurso')
#     idalumno = request.args.get('alumno')
#     alumno = Estudiante.query.filter_by(id=idalumno).first()
#     correo_preceptor = session.get("preceptor")
#     preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
#     idpreceptor = preceptor.id
#     return render_template('confirmar_asistencia.html', fecha=fecha, codigoclase=codigoclase, alumno=alumno, idcurso=idcurso, idalumno=idalumno, preceptor=idpreceptor)


# @app.route('/confirmar_asistencia', methods=['POST'])
# def confirmar_asistencia():
#     idcurso = request.form.get('idcurso')
#     asistencia = Asistencia(fecha=request.form.get('fecha'), codigoclase=request.form.get('codigoclase'), asistio=request.form['asis'], justificacion=request.form['justificacion'], idestudiante=request.form.get('idalumno'))
#     db.session.add(asistencia)
#     db.session.commit()
#     cursos = Curso.query.all()
#     correo_preceptor = session.get("preceptor")
#     preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
#     return redirect(url_for('registrar_asistencia', cursos=cursos, preceptor=preceptor, fecha=request.form.get('fecha'), codigoclase=request.form.get('codigoclase')))
@app.route('/registrar_asistencia')
def registrar_asistencia():
    correo_preceptor = session.get("preceptor")
    preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
    cursos = Curso.query.filter_by(idpreceptor=preceptor.id).all()
    return render_template('cursoclase.html', cursos=cursos, preceptor=preceptor)


@app.route('/asistencia_curso',methods=['POST','GET'])
def asistencia_curso():
    idpreceptor = request.args.get('idpreceptor')
    correo_preceptor = session.get("preceptor")
    fecha = request.form['fecha']
    codigoclase = request.form['tipoclase']
    preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
    idcurso = request.form.get('cursos')
    curso = Curso.query.filter_by(id=idcurso).first()
    alumnos = Estudiante.query.all()
    return render_template('asistencia_curso.html', curso=curso, fecha=fecha, codigoclase=codigoclase, alumnos=alumnos, preceptor=preceptor)


@app.route('/asistencia_alumno', methods=['GET','POST'])
def asistencia_alumno():
    fecha = request.args.get('fecha')
    codigoclase = request.args.get('codigoclase')
    idcurso = request.args.get('idcurso')
    idalumno = request.args.get('alumno')
    alumno = Estudiante.query.filter_by(id=idalumno).first()
    correo_preceptor = session.get("preceptor")
    preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
    idpreceptor = preceptor.id
    return render_template('confirmar_asistencia.html', fecha=fecha, codigoclase=codigoclase, alumno=alumno, idcurso=idcurso, idalumno=idalumno, preceptor=idpreceptor)



@app.route('/confirmar_asistencia', methods=['POST'])
def confirmar_asistencia():
    fecha=request.form.get('fecha')
    ano,mes,dia=map(int,fecha.split('-'))
    fecha=date(ano,mes,dia)
    codigoclase=request.form.get('codigoclase')
    idcurso = request.form.get('idcurso')
    asistencia = Asistencia(fecha=fecha, codigoclase=codigoclase, asistio=request.form['asis'], justificacion=request.form['justificacion'], idestudiante=request.form.get('idalumno'))
    print(fecha)
    print(codigoclase)
    db.session.add(asistencia)
    db.session.commit()
    cursos = Curso.query.all()
    correo_preceptor = session.get("preceptor")
    preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
    return redirect(url_for('registrar_asistencia', cursos=cursos, preceptor=preceptor, fecha=request.form.get('fecha'), codigoclase=request.form.get('codigoclase')))


    
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
    correo_preceptor = session.get("preceptor")
    preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
    return render_template('listar.html', curso=curso, alumnos=alumnos,asistencia=asistencia,preceptor=preceptor)


if __name__=='__main__':
    app.run(debug=True)