from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

class Curso(db.Model):
    __tablename__='curso'
    id = db.Column(db.Integer,primary_key=True)
    año = db.Column(db.Integer,nullable=False)
    division= db.Column(db.Integer,nullable=False)
    idpreceptor=db.Column(db.Integer,db.ForeignKey('Preceptor.id'))
    
class Estudiante(db.Model):
    __tablename__='estudiante'
    id = db.Column(db.Integer,primary_key=True)
    nombre= db.Column(db.String(120),nullable=False)
    apellido = db.Column(db.String(120),nullable=False)
    dni = db.Column(db.String(12),nullable=False)
    idcurso = db.Column(db.Integer,db.ForeignKey('Curso.id'))

class Asistencia(db.Model):
    __tablename__='asistencia'
    id=db.Column(db.Integer,primary_key=True)
    fecha = db.Column(db.Date,nullable=False)
    codigoclase = db.relationship('codigoclase',backref='Curso')
    asistio = db.Column(db.Boolean,nullable=False)
    justificacion=db.Column(db.String(100),nullable=True)
    idestudiante=db.relationship('idestudiante',backref='Estudiante')
    
    
class Preceptor(db.Model):
    __tablename__='preceptor'
    id = db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(100),nullable=False)
    apellido=db.Column(db.String(100),nullable=False)
    correo = db.Column(db.String(100),nullable=False)
    clave = db.Column(db.String(100),nullable=False)