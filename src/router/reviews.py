from flask import request,jsonify
from models import db, Reviews, Userpro

def reviews_route(app,token_required):

    @app.route('/reviews', methods=['POST'])
    @token_required
    def new_review(user):
        body = request.get_json()
        print(body,user)
        id_users = str(user["id"])+"@"+str(body["id"])
        new_review = Reviews(id_traveler=user["id"], id_pro=body["id"],id_users=id_users, value=body["value"])
        userpro = Userpro.query.filter_by(id=body["id"]).first()
        
        old_total = userpro.total_reviews
        new_total = old_total+1
        old_sum = userpro.sum_reviews
        new_sum = old_sum+body["value"]
        old_percent = userpro.percent_reviews
        new_percent = round(new_sum/new_total,1)

        userpro.total_reviews = new_total
        userpro.sum_reviews = new_sum
        userpro.percent_reviews = new_percent

        db.session.add(new_review)
        db.session.add(userpro)
        db.session.commit()

        return jsonify("review added"), 200