from flask import request,jsonify
from encrypted import encrypted_pass, compare_pass
from jwt_auth import generate_token, decode_token
from models import db, Traveler

def traveler_route(app,token_required):#esta función recibe app y token_required que vienen de main

    @app.route('/user/traveler', methods=['POST'])
    def new_traveler():
        body= request.get_json()
        new_user = Traveler(username=body["username"],email=body["email"],password=body["password"],avatar=body["avatar"])
        db.session.add(new_user)
        db.session.commit()
        print(new_user.serialize())

        return jsonify("todo bien"), 200

    @app.route('/traveler/login', methods=['POST'])
    def login_traveler():
        body = request.get_json()
        traveler = Traveler.query.filter_by(email=body['email']).first()
        print(traveler)
        if(traveler is None):
            return "el usuario no existe", 401
        is_validate = compare_pass(body['password'], encrypted_pass(traveler.password).decode("utf-8"))
        if(is_validate == False):
            return "password incorrecto", 401

        token = generate_token(traveler.email, app.config['SECRET_KEY'])
        print(token)
        return jsonify({"access_token":token}), 200