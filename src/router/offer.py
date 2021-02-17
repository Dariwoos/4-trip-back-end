import os
from flask import request,jsonify
from models import db, Offers
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict

host = "https://3000-orange-egret-6bph6z4j.ws-eu03.gitpod.io/"

def offer_route(app,token_required):
    @app.route('/publishoffer', methods=['POST'])
    @token_required
    def new_offer(user):
        try:
            body = dict(request.form)
            print(body,"body")
            print(request.files, "request file")
            if(body["oferta"] is None):
                return jsonify({"msg":"debes describir una oferta"}),400
            f = request.files['attached']
            filename= secure_filename(f.filename)
            f.save(os.path.join("./src/img",filename))
            img_url = host+filename
            print(user, "user")
            new_offer = Offers(text=body['oferta'],attached=img_url,id_trip=body["id_trip"],id_pro=user['id'])
            db.session.add(new_offer)
            db.session.commit()
            print(new_offer.serialize(),"new offer serialize")
            return jsonify(new_offer.serialize()),200

        except OSError as error:
            return jsonify("Error"), 400
