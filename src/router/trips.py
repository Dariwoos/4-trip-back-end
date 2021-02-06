from flask import request,jsonify
from models import db, Trip

def trips_route(app,token_required):

    @app.route('/viajes/<int:page>', methods=['GET'])
    def get_trips(page):
        total_viajes = Trip.query.order_by(Trip.post_date.desc()).paginate(page,3,error_out=False)
        print(total_viajes.items)
        list_trips = []
        for trip in total_viajes.items:
            trip_json = trip.serialize()
            trip_json["needs_trip"]=trip_json["needs_trip"].split(',')
            list_trips.append(trip_json)

        response_body = {
            "data": list_trips
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
