import os
from os.path import join
from flask import request,jsonify
from models import db, Traveler
from encrypted import encrypted_pass
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict

host = "https://3000-d6620844-473e-4005-a216-c78a8882d46d.ws-eu03.gitpod.io/"

def traveler_route(app,token_required):#esta función recibe app y token_required que vienen de main

    @app.route('/user/register/traveler', methods=['POST'])
    def new_traveler():
        try:
            body= request.get_json()
            if body["username"] == "":
                return jsonify({"msg":"usuario no es valido"})
            if body["email"] == "":
                return jsonify({"msg":"correo no es valido"})
            if body["password"] == "":
                return jsonify({"msg":"contraseña no es valido"})
            encrypt_pass = encrypt_pass(body["password"]) 
            f = request.files["avatar"]
            filename= secure_filename(f.filename)
            f.save(os.path.join('./src/img',filename))
            img_url = host + filename
            new_user = Traveler(username=body["username"],email=body["email"],password=body["password"],avatar=body["avatar"])
            db.session.add(new_user)
            db.session.commit()
            print(new_user.serialize())
            return jsonify("todo bien"), 200
        except OSError as error:
            return jsonify("Error"), 400
        except KeyError as error:
            return jsonify("Error Key" + str(error)),400
        
    @app.route('/traveler/<int:id>', methods=['GET'])
    def get_traveler(id):
        body= request.get_json()
        user_traveler = Traveler.query.filter_by(id=id).first()
        if user_traveler is not None:
            return jsonify(user_traveler.serialize()),200
        else:
            return jsonify("usaurio no existe"),400
    
    @app.route('/traveler/<int:id>',methods=['PUT'])
    def edit_account_traveler():
        body = request.get_json()
        user_traveler= Traveler.query.filter_by(id=id).first()
        if user_traveler is not None:
            for key in body:
                setattr(user_traveler,key,body[key])
            db.session.commit()
            return jsonify(user_traveler.serialize()),200
        else:
            return jsonify("usuario no existe")

