from flask import render_template
from flask import Flask

app=Flask('pagina')

@app.route('/')
def saludo():
    return render_template('inicio.html')

@app.route('/preceptor')
def paginapreceptor():
    return render_template('paginapreceptor.html')

@app.route('/tutor')
def paginatutor():
    return render_template('paginatutor.html')


if __name__=='__main__':
    app.run()