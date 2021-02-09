import os
from os.path import join
from flask import request,jsonify
from models import db, Traveler
from encrypted import encrypted_pass
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import base64

host = "https://3000-d6620844-473e-4005-a216-c78a8882d46d.ws-eu03.gitpod.io/"

def traveler_route(app,token_required):#esta función recibe app y token_required que vienen de main

    @app.route('/user/register/traveler', methods=['POST'])
    def new_traveler():
        try:
            new_object = request.get_json()
            print(new_object)
            data = request.data
            print(type(data.decode("utf-8")))
            body = request.get_json()
            print(body,"body")
            if body["username"] == "":
                return jsonify({"msg":"usuario no es valido"}),400
            if body["email"] == "":
                return jsonify({"msg":"correo no es valido"}),400
            if body["password"] == "":
                return jsonify({"msg":"contraseña no es valida"}),400
            print("funciona")
            encrypt_pass = encrypted_pass(body["password"]) 
            print("antes del img")
            img = body["avatar"]
            f = base64.b64encode(img.read())
            filename= secure_filename(f.filename)
            print(filename)
            f.save(os.path.join('./src/img',filename))
            img_url = host+filename
            print(img_url,"url")
            new_user = Traveler(username=body["username"],email=body["email"],password=body["password"],avatar=img_url)
            print(new_user)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(new_user.serialize()), 200
        except OSError as error:
            return jsonify("Error"), 400
        except KeyError as error:
            return jsonify("Error Key" + str(error)),400
        
    @app.route('/traveler', methods=['GET'])
    @token_required
    def get_traveler(user):
        #body = request.get_json()
        user_traveler = Traveler.query.filter_by(id=user["id"]).first()
        if user_traveler is not None:
            return jsonify(user_traveler.serialize()),200
        else:
            return jsonify("usaurio no existe"),400
    
    @app.route('/traveler',methods=['PUT'])
    @token_required
    def edit_account_traveler(user):
        print(user)
        body = request.get_json()
        user_traveler= Traveler.query.filter_by(id=user["id"]).first()
        if user_traveler is not None:
            for key in body:
                print(key,"key")
                setattr(user_traveler,key,body[key])
            db.session.commit()
            return jsonify(user_traveler.serialize()),200
        else:
            return jsonify("usuario no existe")

