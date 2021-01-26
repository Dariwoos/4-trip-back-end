from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime, date

db = SQLAlchemy()

class Traveler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(15), unique=False, nullable=False)
    avatar = db.Column(db.String(200), unique=False, nullable=True)
    rol = db.Column(db.String(10), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    trip = relationship("Trip")
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self,username,email,password,avatar,rol,is_active):
        self.username = username
        self.email = email
        self.password = password
        self.avatar = avatar
        self.rol = rol
        self.is_active = True

    def __repr__(self):
        return '<Traveler %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "avatar": self.avatar,
            "rol": self.rol,
        }

class Trip(db.Model): #aqui no meto is_active, post_date ni receiving_offers porque no se lo estoy pasando a través de main ya que son campos que van con un valor por defecto
    id = db.Column(db.Integer, primary_key=True)
    id_traveler = db.Column(db.Integer, db.ForeignKey('traveler.id'))
    is_active = db.Column(db.Boolean(), default=True, unique=False, nullable=False)
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    needs_trip = db.Column(db.String(60), unique=False, nullable=False)
    destination = db.Column(db.String(200), unique=False, nullable=False)
    first_day = db.Column(db.Date(), unique=False, nullable=False)
    last_day = db.Column(db.Date(), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)
    receiving_offers = db.Column(db.Boolean(), default=True, unique=False, nullable=False)

    def __init__(self,needs_trip,destination,first_day,last_day,description):
        self.needs_trip = needs_trip
        self.destination = destination
        self.first_day = first_day
        self.last_day = last_day
        self.description = description
    
    def __repr__(self):
        return '<Trip %r>' % self.id


    def serialize (self):
        return {
            "id": self.id,
            "id_traveler": self.id_traveler,
            "post_date": self.post_date,
            "needs_trip": self.needs_trip,
            "destination": self.destination,
            "first_day": self.first_day,
            "last_day": self.last_day,
            "description": self.description,
        }