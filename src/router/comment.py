from flask import request,jsonify
from models import db, Offers
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict

host = "https://3000-orange-egret-6bph6z4j.ws-eu03.gitpod.io/"

def offer_route(app,token_required):
    @app.route('/publishcomment', methods=['POST'])
    @token_required
    def new_offer(user):
        try:
            body = dict(request.form)
            print(body, "BODY")
            if(body["comment"] is None):
                return jsonify({"msg":"debes escribir un comentario"}),400
            if(len(request.files)!=0):
                f = request.files['attached']
                filename= secure_filename(f.filename)
                f.save(os.path.join("./src/img",filename))
                img_url = host+filename
                new_comment = Comments(text=body['comment'],attached=img_url,id_traveler=body["id_traveler"],id_pro=user['id'],id_offer=["id_offer"])
            else: new_offer = Comments(text=body['comment'],id_traveler=body["id_traveler"],id_pro=user['id'],id_offer=["id_offer"])
            db.session.add(new_comment)
            db.session.commit()
            return jsonify(new_comment.serialize()),200

        except OSError as error:
            return jsonify("Error"), 400