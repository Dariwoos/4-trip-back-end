from flask_sqlalchemy import SQLAlchemy
import datetime
#from flask_appbuilder import Model

db = SQLAlchemy()

class Userpro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(35), unique=True, nullable=False)
    password = db.Column(db.String(40), unique=False, nullable=False)
    phone= db.Column(db.String(20), unique = True , nullable=False)
    url = db.Column(db.String(50))
    location = db.Column(db.String(40) , nullable= False)
    direction = db.Column(db.String(40), nullable=False)
    vat_number = db.Column(db.String(20))
    social_reason = db.Column(db.String(20))
    avatar= db.Column(db.String(100), nullable=False)
    photos = db.Column(db.String(200))
    registr_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    rol = db.Column(db.String(30))
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    Ofertas = db.relationship("Offers")

    def __init__(self,username,email,password,phone,url,location,direction,vat_number,social_reason,avatar,photos,registr_date,rol,is_active):
        self.user_name = username
        self.email = email
        self.password = password
        self.phone = phone
        self.url= url
        self.location = location
        self.direction = direction
        self.vat_number = vat_number
        self.social_reason =social_reason
        self.avatar = avatar
        self.photos = photos
        self.registr_date = registr_date
        self.rol = rol
        self.is_active = True

    def __repr__(self):
        return '<Userpro%r>' % self.username

    def serialize(self,user_name,email,password,phone,url,location,direction,vat_number,social_reason,avatar,photos,registr_date,rol):
        return {
            "id": self.id,
            "user_name":self.user_name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "url": self.url,
            "location": self.location,
            "direction":self.direction,
            "vat_number":self.vat_number,
            "social_reason": self.social_reason,
            "avatar": self.avatar,
            "photos": self.photos,
            "registr_date": self.registr_date,
            "rol": self.rol
            # do not serialize the password, its a security breach
        }

class Offers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_pro =db.Column(db.Integer, db.ForeignKey("userpro.id"), nullable=False)
    #id_trip = db.Column(db.Integer, db.ForeignKey(""),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow)
    text = db.Column(db.String(200),nullable=False)
    counter = db.Column(db.Integer,nullable=False)

    def __init__(self,date,text,counter):
        self.date: date
        self.text: text
        self.counter: counter

    def __repr__(self):
        return '<Offers%r>' % self.username

    def serialize(self,date,text,counter):
        return {
            "date":self.date,
            "text":self.text,
            "counter":self.counter
            # do not serialize the password, its a security breach
        }