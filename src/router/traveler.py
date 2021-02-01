from flask import request,jsonify
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