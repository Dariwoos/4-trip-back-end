from flask import request,jsonify
from models import db, Trip, Traveler

def trips_route(app,token_required):

    @app.route('/viajes/<int:page>', methods=['GET'])
    def get_trips(page):
        total_viajes = Trip.query.order_by(Trip.post_date.desc()).paginate(page,3,error_out=False)
        if len(total_viajes.items) == 0:
            respose = {
                "data":[]
            }
            return jsonify(respose), 200
        print(total_viajes)
        list_trips = []
        for trip in total_viajes.items:
            print(trip, "TRIP")
            trip_json = trip.serialize()
            trip_json["needs_trip"]=trip_json["needs_trip"].split(',')
            list_trips.append(trip_json)
        print(type(list_trips[0]["needs_trip"]), "@@@@@@@@@@@@@@@")
        response_body = {
            "data": list_trips
        }

        return jsonify(response_body), 200

    #TODO: VALIDACIONES DE LOS CAMPOS PARA CREAR EL VIAJE Y USAR EL TRY - EXCEPT
    @app.route('/viaje', methods=['POST'])
    @token_required
    def post_trip(user):
        body = request.get_json()
        new_trip = Trip(id_traveler=user['id'], needs_trip=body['needs_trip'], destination=body['destination'], first_day=body['first_day'], last_day=body['last_day'], description=body['description'])
        db.session.add(new_trip)
        db.session.commit()
        print(new_trip.serialize())
        new_travel_json = new_trip.serialize()
        return jsonify(new_travel_json), 200

    @app.route('/viaje/<int:id>', methods=['GET'])
    def get_trip(id):
        detail_trip = Trip.query.filter_by(id=id).first()
        trip_json=detail_trip.serialize()
        trip_json["needs_trip"]=trip_json["needs_trip"].split(',')#needs_trip que está dentro de trip_json lo convierto en array porque está como string
        if trip_json is not None:
            return jsonify(trip_json),200
        return "not found", 404

