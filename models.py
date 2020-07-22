""" Modelo """
from .app import db

class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(180), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return '<Nombre %r>' % self.nombre