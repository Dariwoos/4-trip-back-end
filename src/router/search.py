from flask import request,jsonify
from models import db, Trip

def search_route(app):

    @app.route('/search', methods=["POST"])
    def search():
        body=request.get_json()
        trips = Trip.query.filter(Trip.destination.like('%'+body["destination"]+'%')).all()
        trip_list = []
        for trip in trips:
            trip_search = trip.serialize()
            trip_search["needs_trip"] = trip_search["needs_trip"].split(',')
            trip_list.append(trip_search)
               
        if len(trip_list)>0:
            return jsonify(trip_list),200
        return "not found", 404