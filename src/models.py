from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import datetime

#from flask_appbuilder import Model

db = SQLAlchemy()

class Userpro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(35), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    phone= db.Column(db.String(20), unique = True , nullable=False)
    url = db.Column(db.String(120))
    location = db.Column(db.String(40) , nullable= False)
    direction = db.Column(db.String(40), nullable=False)
    vat_number = db.Column(db.String(20), nullable=True)
    social_reason = db.Column(db.String(20),nullable=True)
    avatar= db.Column(db.String(120), nullable=False)
    photos = db.Column(db.Text)
    registr_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    rol = db.Column(db.String(30),default="Profesional")
    is_active = db.Column(db.Boolean(), unique=False, nullable=False,default=True)
    #percent_reviews = db.Column(db.Float(), nullable=False, default=5)
    #total_reviews = db.Column(db.Float(), nullable=True, default=0) este seria la unica columna que necesito
    #sum_reviews = db.Column(db.Integer, nullable=False, default=5)
    offers = db.relationship("Offers")
    comments = relationship('Comments')
      
     
    def serialize(self):
        return {
            "id": self.id,
            "user_name":self.user_name,
            "email": self.email,
            "phone": self.phone,
            "url": self.url,
            "location": self.location,
            "direction":self.direction,
            "vat_number":self.vat_number,
            "social_reason": self.social_reason,
            "avatar": self.avatar,
            "photos": self.photos,
            "registr_date": self.registr_date,
            "rol": self.rol,
            # do not serialize the password, its a security breach
        }

    def json_to_offer(self):
        return{
            "avatar": self.avatar,
            "user_name": self.user_name,
            "id": self.id
        }
      
      
     

class Traveler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    avatar = db.Column(db.String(180), nullable=True)
    rol = db.Column(db.String(10), nullable=False, default= "Traveler")
    is_active = db.Column(db.Boolean(), default=True ,unique=False, nullable=False)
    trip = relationship("Trip")
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    comments = relationship('Comments')

    def __init__(self,username,email,password,avatar):
        self.username = username
        self.email = email
        self.password = password
        self.avatar = avatar
        #self.is_active = True

    
    def __repr__(self):
        return '<Traveler %r>' % self.username

    def password_bcrypt(self):
        return self.password

    def serialize(self): 
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "avatar": self.avatar,
            #"rol": self.rol,   
            "create_date":self.fecha_registro,
        }

    def json_to_offer(self):
        return {
            "id": self.id,
            "username": self.username,
            "avatar": self.avatar
        }

class Offers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_pro =db.Column(db.Integer, db.ForeignKey("userpro.id"), nullable=False)
    id_trip = db.Column(db.Integer, db.ForeignKey("trip.id"),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow)
    text = db.Column(db.Text,nullable=False)
    attached = db.Column(db.String(120), nullable=True)
    comments = db.relationship("Comments", backref="Offers", lazy=True) #así accedo a comentarios y los puedo listar
    userpro = db.relationship("Userpro", backref="Offers", lazy=True)

        
    def __repr__(self):
        return '<Offers %r>' % self.id

    def serialize(self):
        return {
            "id":self.id,
            "date":self.date,
            "text":self.text,
            "date":self.date,
            "id_pro":self.id_pro,
            "id_trip":self.id_trip,
            "attached":self.attached,
            "comments": list(map(lambda x: x.serialize(),self.comments)),
            "userpro": self.userpro.json_to_offer()
        }

class Trip(db.Model): #aqui no meto is_active, post_date ni receiving_offers porque no se lo estoy pasando a través de main ya que son campos que van con un valor por defecto
    id = db.Column(db.Integer, primary_key=True)
    id_traveler = db.Column(db.Integer, db.ForeignKey('traveler.id'))
    is_active = db.Column(db.Boolean(), default=True, unique=False, nullable=False)
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    needs_trip = db.Column(db.String(60), unique=False, nullable=False)
    destination = db.Column(db.String(200), unique=False, nullable=False)
    first_day = db.Column(db.Date(), unique=False, nullable=False)
    last_day = db.Column(db.Date(), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)
    receiving_offers = db.Column(db.Boolean(), unique=False, default=True, nullable=False)
    traveler = db.relationship('Traveler', backref='Trip', lazy=True) #así accedo a la tabla de traveler
    offers = db.relationship("Offers", backref="Trip", lazy=True) #así accedo a ofertas y las puedo listar
    counter = db.Column(db.Integer,nullable=False)

    def __init__(self,id_traveler,needs_trip,destination,first_day,last_day,description):
        self.id_traveler = id_traveler
        self.is_active = True
        self.needs_trip = needs_trip
        self.destination = destination
        self.first_day = first_day
        self.last_day = last_day
        self.description = description
        self.counter = 0

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
            "counter":self.counter,
            "receiving_offers":self.receiving_offers,
            "traveler": self.traveler.serialize(),
            "offers": list(map(lambda x: x.serialize(),self.offers))
        }

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_traveler = db.Column(db.Integer, db.ForeignKey('traveler.id'),nullable=True)
    id_pro = db.Column(db.Integer, db.ForeignKey('userpro.id'),nullable=True)
    id_offer = db.Column(db.Integer, db.ForeignKey('offers.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow)
    text = db.Column(db.Text,nullable=False)
    attached = db.Column(db.String(120), nullable=True)
    traveler = db.relationship('Traveler', backref='Comments', lazy=True) #así accedo a la tabla de traveler
    userpro = db.relationship("Userpro", backref="Comments", lazy=True) #así accedo a  la tabla de userpro

    def __repr__(self):
        return '<Comments %r>' % self.id


    def serialize (self):
        return {
            "id": self.id,
            "id_traveler": self.id_traveler,
            "id_pro": self.id_pro,
            "id_offer": self.id_offer,
            "date": self.date,
            "text": self.text,
            "attached":self.attached,
            "traveler": self.traveler.json_to_offer() if self.traveler is not None else None,#esto es un ternario. Si la condicion, que es lo que esta a la derecha del if, es veradera se ejecuta lo que está a la izquierda del if, si es falsa lo que esta despues de else 
            "userpro": self.userpro.json_to_offer() if self.userpro is not None else None
        }

    #VALORACIONES
    #10 reseñas 2,4,5,5,4,3,2,2,1,5
    #33puntos sobre reseñas *5
    #5:50=x:33
    #(33*5)/50

    class Reviews(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        id_traveler = db.Column(db.Integer, db.ForeignKey('traveler.id'),nullable=False)
        id_pro = db.Column(db.Integer, db.ForeignKey('userpro.id'),nullable=False)
        value = db.Column(db.Integer, nullable=False)
        traveler = db.relationship('Traveler')
        userpro = db.relationship("Userpro")
    