from flask import request,jsonify
from models import db, Trip

def search_route(app):

    @app.route('/search', methods=["POST"])
    def search():
        body=request.get_json()
        trips = Trip.query.filter(Trip.destination.like('%'+body["search"]+'%')).all()
        print(trips)
        list_trips =[]
        for trip in trips:
            list_trips.append(trip.serialize())
        return jsonify(list_trips)