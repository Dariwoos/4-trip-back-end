import os
from flask import request,jsonify
from models import db, Offers
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from send_email import sendEmail

host = "https://3000-orange-egret-6bph6z4j.ws-eu03.gitpod.io/"

def offer_route(app,token_required):
    @app.route('/publishoffer', methods=['POST'])
    @token_required
    def new_offer(user):
        try:
            body = dict(request.form)
            print(body, "BODY@@@@@@@@@@@@@@@@@@@@@@")
            if(body["oferta"] is None):
                return jsonify({"msg":"debes describir una oferta"}),400
            if(len(request.files)>0):
                f = request.files['attached']
                filename= secure_filename(f.filename)
                f.save(os.path.join("./src/img",filename))
                img_url = host+filename
                new_offer = Offers(text=body['oferta'],attached=img_url,id_trip=body["id_trip"],id_pro=user['id'])
            else: new_offer = Offers(text=body['oferta'],id_trip=body["id_trip"],id_pro=user['id'])
            db.session.add(new_offer)
            db.session.commit()
            sendEmail(body["email"])
            return jsonify(new_offer.serialize()),200

        except OSError as error:
            return jsonify("Error"), 400
