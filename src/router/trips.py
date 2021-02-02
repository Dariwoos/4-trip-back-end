from flask import request,jsonify
from models import db, Trip

def trips_route(app,token_required):

    @app.route('/viajes', methods=['GET'])
    def get_trips():
        total_viajes = Trip.query.all()

        response_body = {
            "msg": "estos son todos los viajes"
        }

        return jsonify(response_body), 200

    #TODO: VALIDACIONES DE LOS CAMPOS PARA CREAR EL VIAJE Y USAR EL TRY - EXCEPT
    @app.route('/viaje', methods=['POST'])
    @token_required
    def post_trip(user):
        print("este es el user",user)
        body = request.get_json()
        new_trip = Trip(id_traveler=user['id'], needs_trip=body['needs_trip'], destination=body['destination'], first_day=body['first_day'], last_day=body['last_day'], description=body['description'])
        db.session.add(new_trip)
        db.session.commit()
        print(new_trip.serialize())

        return jsonify(new_trip.serialize()), 200
