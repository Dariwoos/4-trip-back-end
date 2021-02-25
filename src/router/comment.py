from flask import request,jsonify
from models import db, Comments
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict

host = "https://fortrips.herokuapp.com/"

def comment_route(app,token_required):

    @app.route('/publishcomment', methods=['POST'])
    @token_required
    def create_comment(user):
        try:
            body = dict(request.form)
            print(body)
            if(body["comment"] is None):
                return jsonify({"msg":"debes escribir un comentario"}),400
            # img
            if(len(request.files)>0):
                f = request.files['attached']
                filename= secure_filename(f.filename)
                f.save(os.path.join("./img",filename))
                img_url = host+filename
                if user['rol'] != 'Profesional':
                    new_comment = Comments(text=body['comment'],attached=img_url,id_traveler=user['id'], id_pro=None,id_offer=body["id_offer"])
                else:
                    new_comment = Comments(text=body['comment'],attached=img_url,id_traveler=None,id_pro=user['id'],id_offer=body["id_offer"])
            else:
                #not image
                if user['rol'] != 'Profesional': 
                    new_comment = Comments(text=body['comment'],id_traveler=user['id'],id_pro=None,id_offer=body["id_offer"])
                else:
                    new_comment = Comments(text=body['comment'],id_traveler=None,id_pro=user['id'],id_offer=body["id_offer"])

            db.session.add(new_comment)
            db.session.commit()
            return jsonify(new_comment.serialize()),200

        except OSError as error:
            print('error', error)
            return jsonify("Error"), 400

        except Exception as err:
            print(err)
            return jsonify("Error"), 500