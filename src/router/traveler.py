import os
from os.path import join
from flask import request,jsonify
from models import db, Traveler
from encrypted import encrypted_pass
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import base64
from cloudinary_funct import save_image

host = "https://fortrips.herokuapp.com/"

def traveler_route(app,token_required):#esta función recibe app y token_required que vienen de main

    @app.route('/user/register/traveler', methods=['POST'])
    def new_traveler():
        try:
            body = dict(request.form)
            if body["username"] == "":
                return jsonify({"msg":"usuario no es valido"}),404
            if body["email"] == "":
                return jsonify({"msg":"correo no es valido"}),404
            if body["password"] == "":
                return jsonify({"msg":"contraseña no es valida"}),404
            if request.files:
                f = request.files['avatar']
                img_url=save_image(f)
            else:
                img_url = "https://res.cloudinary.com/dyfwsdqx8/image/upload/v1615318577/default_avatar_okufrf.png"
            encrypt_pass = encrypted_pass(body["password"])      
            new_user = Traveler(username=body["username"],email=body["email"],password=encrypt_pass,avatar=img_url)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(new_user.serialize()), 200
        except OSError as error:
            print(error)
            return jsonify("Error"), 400
        except KeyError as error:
            print(error)
            return jsonify("Error Key" + str(error)),400
        
    @app.route('/traveler', methods=['GET'])
    @token_required
    def get_traveler(user):
        user_traveler = Traveler.query.filter_by(id=user["id"]).first()
        if user_traveler is not None:
            return jsonify(user_traveler.serialize()),200
        else:
            return jsonify("usaurio no existe"),400
    
    @app.route('/traveler',methods=['PUT'])
    @token_required
    def edit_account_traveler(user):
        body = dict(request.form)
        if request.files:
            f = request.files['avatar']
            img_url = save_image(f)
        user_traveler= Traveler.query.filter_by(id=user["id"]).first()
        if user_traveler is not None:
            for key in body:
                setattr(user_traveler,key,body[key])
            db.session.commit()
            return jsonify(user_traveler.serialize()),200
        else:
            return jsonify("usuario no existe")

