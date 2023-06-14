from flask import render_template
from flask import Flask

app=Flask('pagina')

@app.route('/')
def saludo():
    return render_template('inicio.html')


if __name__=='__main__':
    app.run()