from flask import render_template
from flask import Flask,request


app=Flask('pagina')
app.config.from_pyfile('config.py')

from modelos import db
from modelos import Curso,Estudiante,Padre,Preceptor,Asistencia

@app.route('/')
def saludo():
    return render_template('inicio.html')

@app.route('/preceptor',methods= ['POST','GET'])
def paginapreceptor():
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
@app.route('/tutor')
def paginatutor():
    return render_template('paginatutor.html')


if __name__=='__main__':
    db.create_all()
    app.run(debug=True)