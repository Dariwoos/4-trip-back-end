"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for,send_file
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Traveler, Trip, Userpro, Offers, Comments

#from models import Person

from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict

from router.professional import professional_route
from router.traveler import traveler_route
from router.trips import trips_route
from router.login import login_route
from router.offer import offer_route
import jwt_auth
import jwt

from functools import wraps #importacion para generar el decorador

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Yu9M@*tU<Z0VavW0!'
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

#decorador
def token_required(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        try:
            auth = request.headers.get('Authorization')
            if auth is None:
                return jsonify('no token'),403
            token = auth.split(' ')
            data = jwt_auth.decode_token(token[1], app.config['SECRET_KEY'])
            if data["rol"] == "Traveler":
                traveler = Traveler.query.filter_by(email=data["email"]).first()
                if traveler is None:
                    return jsonify("no authorization"), 401
            elif data["rol"] == "Profesional":
                pro = Userpro.query.filter_by(email=data["email"]).first()
                if pro is None:
                    return jsonify("no authorization"), 401

            print("DATAAAA",data)
            print("token_required", data)
            return f(data, *args, **kwargs)#meto toda la data para pasar en el token el id del usuario

        except OSError as error:
            print(error)

        except jwt.ExpiredSignatureError as err:
            print(err)
            return jsonify("token expired"), 403
            
    return decorador

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/<filename>",methods=["GET"])
def photo_rout_pro(filename):
    return send_file("./img/"+filename)


#llamo a las funciones creadas en la carpeta route y las paso los parámetros app y token_required
proffesional = professional_route(app,token_required)
traveler = traveler_route(app,token_required)
trips = trips_route(app,token_required)
login = login_route(app)#no necesitamos token. El token solo lo necesitamos cuando las funciones requieren estar logueado
offer = offer_route(app,token_required)


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
