from flask import request,jsonify

def trips_route(app,token_required):

    @app.route('/viajes', methods=['GET'])
    def get_trips():
        total_viajes = Trip.query.all()

        response_body = {
            "msg": "estos son todos los viajes"
        }

        return jsonify(response_body), 200

    @app.route('/viaje', methods=['POST'])
    @token_required
    def post_trip():
        body = request.get_json()
        print(Trip(needs_trip=body['needs_trip'], destination=body['destination'], first_day=body['first_day'], last_day=body['last_day'], description=body['description']))
        new_trip = Trip(needs_trip=body['needs_trip'], destination=body['destination'], first_day=body['first_day'], last_day=body['last_day'], description=body['description'])
        db.session.add(new_trip)
        db.session.commit()
        print(new_trip.serialize())

        return jsonify(new_trip.serialize()), 200
