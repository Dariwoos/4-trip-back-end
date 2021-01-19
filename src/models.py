from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime, date

db = SQLAlchemy()

class Viajero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(15), unique=False, nullable=False)
    avatar = db.Column(db.String(200), unique=False, nullable=True)
    rol = db.Column(db.String(10), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    trip = relationship("Viaje")
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self,username,email,password,avatar,rol,is_active):
        self.username = username
        self.email = email
        self.password = password
        self.avatar = avatar
        self.rol = rol
        self.is_active = True

    def __repr__(self):
        return '<Viajero %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "avatar": self.avatar,
            "rol": self.rol,
        }

class Viaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_viajero = db.Column(db.Integer, db.ForeignKey('viajero.id'))
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    fecha_publicacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    needs_trip = db.Column(db.String(60), unique=False, nullable=False)
    destination = db.Column(db.String(200), unique=False, nullable=False)
    first_day = db.Column(db.Date(), unique=False, nullable=False)
    last_day = db.Column(db.Date(), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)

    def __init__(self,is_active,fecha_publicacion,needs_trip,destination,first_day,last_day,description):
        self.is_active = True
        self.fecha_publicacion = fecha_publicacion
        self.needs_trip = needs_trip
        self.destination = destination
        self.first_day = first_day
        self.last_day = last_day
        self.description = description
    
    def __repr__(self):
        return '<Viaje %r>' % self.id

    def serialize (self):
        return {
            "id": self.id,
            "id_viajero": self.id_viajero,
            "fecha_publicacion": self.fecha_publicacion,
            "needs_trip": self.needs_trip,
            "destination": self.destination,
            "first_day": self.first_day,
            "last_day": self.last_day,
            "description": self.description,
        }