import os
from flask import request,jsonify
from models import db, Offers
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from send_email import sendEmail
from cloudinary_funct import save_image

host = "https://fortrips.herokuapp.com/"

def offer_route(app,token_required):
    @app.route('/publishoffer', methods=['POST'])
    @token_required
    def new_offer(user):
        try:
            body = dict(request.form)
            if(body["oferta"] is None):
                return jsonify({"msg":"debes describir una oferta"}),400
            if(len(request.files)>0):
                f = request.files['attached']
                #filename= secure_filename(f.filename)Al usar cloudinary no lo necesito
                #f.save(os.path.join("./img",filename))Al usar cloudinary no lo necesito
                img_url = save_image(f)
                offer = Offers(text=body['oferta'],attached=img_url,id_trip=body["id_trip"],id_pro=user['id'])
            else: 
                offer = Offers(text=body['oferta'],id_trip=body["id_trip"],id_pro=user['id'])
            db.session.add(offer)
            db.session.commit()
            sendEmail(body["email"])
            return jsonify(offer.serialize()),200

        except OSError as error:
            return jsonify("Error"), 400
