from flask import request,jsonify
from models import db, Comments
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict

host = "https://3000-orange-egret-6bph6z4j.ws-eu03.gitpod.io/"

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
            print('files', request.files)
            if(len(request.files)>0):
                f = request.files['attached']
                filename= secure_filename(f.filename)
                f.save(os.path.join("./src/img",filename))
                img_url = host+filename
                if user['rol'] != 'Profesional':
                    new_comment = Comments(text=body['comment'],attached=img_url,id_traveler=user['id'], id_pro=None,id_offer=body["id_offer"])
                else:
                    new_comment = Comments(text=body['comment'],attached=img_url,id_traveler=None,id_pro=user['id'],id_offer=body["id_offer"])
            else:
                #not image
                print('entrnado en el else de img')
                if user['rol'] != 'Profesional': 
                    new_comment = Comments(text=body['comment'],id_traveler=user['id'],id_pro=None,id_offer=body["id_offer"])
                else:
                    print('coment pro')
                    new_comment = Comments(text=body['comment'],id_traveler=None,id_pro=user['id'],id_offer=body["id_offer"])
                    print(new_comment.serialize())
            db.session.add(new_comment)
            db.session.commit()
            return jsonify(new_comment.serialize()),200

        except OSError as error:
            print('error', error)
            return jsonify("Error"), 400

        except Exception as err:
            print(err)
            return jsonify("Error"), 500