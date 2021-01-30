"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Traveler, Trip, Userpro, Offers
from encrypted import encrypted_pass, compare_pass

#from models import Person

from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict

from jwt_auth import generate_token, decode_token

from functools import wraps

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Yu9M@*tU<Z0VavW0!'
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
host = "https://3000-a6e518a6-1f81-4a11-bade-6a56b5be8309.ws-eu03.gitpod.io/"

usuario_fake = {
    "email": "mariocepedaortega@gmail.com",
    "password": encrypted_pass("123456")
}
#decorador
#def token_required(f):
    #@wraps(f)
    #def decorador(*args, **kwargs):
        #try:
            #auth = request.headers.get('Authorization')
            #print(auth)
        #except:
            #pass
        #return f(*args, **kwargs)
    #return decorador

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user/register/pro', methods=['POST'])
def handle_pro():
    body = request.get_json()
    new_user = Userpro(user_name=body['user_name'],password=encrypt_pass, email=body['email'],phone=body['phone'],url=body['url'],location=body['location'],direction=body['direction'],vat_number=body['vat_number'],social_reason=body['social_reason'])
    db.session.add(new_user) #sin este linea no se añade a la base de datos
    db.session.commit() # esta es la hermana de la que esta arriba :) 
    print(new_user.serialize())
    return jsonify(new_user.serialize()),200

@app.route('/user/pro', methods=['GET'])
def get_all_pros():
    body = Userpro.query.all()
    for x in body:
        print(x.serialize())
    print(body)

@app.route('/user/traveler', methods=['POST'])
def handle_Traveler():
    body= request.get_json()
    new_user = Traveler(username=body["username"],email=body["email"],password=body["password"])
    db.session.add(new_user)
    db.session.commit()
    print(new_user.serialize())

    return jsonify("todo bien"), 200
    
@app.route('/pro/<int:id>',methods=['GET'])
def get_pro(id):
    user_pro_by_id = Userpro.query.filter_by(id=id).first()
    print(user_pro_by_id.serialize())
    if user_pro_by_id is not None:
        return jsonify(user_pro_by_id.serialize()), 200
    else:
        return jsonify("usuario no existe"),400

@app.route('/viajes', methods=['GET'])
def get_viajes():
    total_viajes = Trip.query.all()

    response_body = {
        "msg": "estos son todos los viajes"
    }

    return jsonify(response_body), 200

@app.route('/traveler/login', methods=['POST'])
def login_traveler():
    body = request.get_json()
    print(usuario_fake)
    #traveler = Traveler.query.filter_by(email=body['email']).first()
    if(usuario_fake["email"]==body["email"]):
        traveler = usuario_fake
    else:
        traveler = None 
    if(traveler is None):
        return "el usuario no existe", 401
    is_validate = compare_pass(body['password'], traveler["password"].decode("utf-8"))
    if(is_validate == False):
       return "password incorrecto", 401

    token = generate_token(traveler["email"], app.config['SECRET_KEY'])
    #print(token)
    return jsonify({"access_token":token}), 200

@app.route("/publicar/viaje",methods=["POST"])
def creat_trip():
    body = dict(request.form)
    f = request.files["image"] 
    filename = secure_filename(f.filename)
    f.save(os.path.join("./src/img",filename))
    img_url = host + filename
    new_trip = Trip(img_url , body["needs_trip"], body["destination"],body["first_day"],body["last_day"],body["description"],body["id_traveler"])
    print(body)
    print(f)
    print(new_trip)
    return  jsonify ("creando post"),201

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
