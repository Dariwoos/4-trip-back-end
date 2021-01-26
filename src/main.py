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

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

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
    new_user = Userpro(user_name=body['user_name'], email=body['email'],password=body['password'],phone=body['phone'],url=body['url'],location=body['location'],direction=body['direction'],vat_number=body['vat_number'],social_reason=body['social_reason'])
    db.session.add(new_user) #sin este linea no se añade a la base de datos
    db.session.commit() # esta es la hermana de la que esta arriba :) 
    print(new_user.serialize())
    return jsonify(new_user.serialize()),200

@app.route('/user/pro', methods=['GET'])
def handle_hello():
    body = Userpro.query.all()
    for x in body:
        print(x.serialize())
    print(body)
    return jsonify("todo bien"), 200
    
@app.route('/pro/<int:id>',methods=['GET'])
def get_pro(id):
    user_pro_by_id = Userpro.query.filter_by(id=id).filter_by(is_active=False).first()
    print(user_pro_by_id)
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

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
