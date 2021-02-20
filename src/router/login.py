from flask import request,jsonify
from models import db, Traveler, Userpro
from jwt_auth import generate_token
from encrypted import encrypted_pass, compare_pass

def login_route(app):#esta función recibe app y token_required que vienen de main

    @app.route('/login', methods=['POST'])
    def login_traveler():
        body = request.get_json()
        traveler = Traveler.query.filter_by(email=body['email']).first()

        if(traveler is not None):
            is_validate = compare_pass(body['password'],traveler.password)
            
            if(is_validate == False):
                return "password incorrecto", 401        
            token = generate_token(traveler.email,traveler.rol,traveler.id,app.config['SECRET_KEY'])#añado el rol para pasar por el token esta informacion y poder saber si tengo que ir a consultar si el usuario existe a la base de datos de traveler o de professional
            return jsonify({"access_token":token,"rol":traveler.rol}), 200
        pro = Userpro.query.filter_by(email=body["email"]).first()
        print(pro)
        print(pro.serialize())
        print(body)
        print(compare_pass(body['password'],pro.password))
       
        if(pro is not None):
            is_validate = compare_pass(body['password'],pro.password )

            if(is_validate == False):
                return "password incorrecto", 401

            token = generate_token(pro.email,pro.rol,pro.id,app.config['SECRET_KEY'])#añado el rol para pasar por el token esta informacion y poder saber si tengo que ir a consultar si el usuario existe a la base de datos de traveler o de professional
            return jsonify({"access_token":token,"rol":pro.rol}), 200

        return jsonify ("user not exists"), 404