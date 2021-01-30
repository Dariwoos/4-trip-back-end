from flask import request,jsonify
from encrypted import encrypted_pass, compare_pass
from jwt_auth import generate_token, decode_token

def traveler_route(app,token_required):#esta función recibe app y token_required que vienen de main

    @app.route('/user/traveler', methods=['POST'])
    def new_traveler():
        body= request.get_json()
        new_user = Traveler(username=body["username"],email=body["email"],password=body["password"])
        db.session.add(new_user)
        db.session.commit()
        print(new_user.serialize())

        return jsonify("todo bien"), 200

    @app.route('/traveler/login', methods=['POST'])
    def login_traveler():
        usuario_fake = {
            "email": "mariocepedaortega@gmail.com",
            "password": encrypted_pass("123456")
        }
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