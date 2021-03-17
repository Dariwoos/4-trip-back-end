import os
from os.path import join
from flask import request,jsonify
from models import db,Userpro
from encrypted import encrypted_pass
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import base64
from cloudinary_funct import save_image

host = "https://fortrips.herokuapp.com/"

def professional_route(app,token_required):

    @app.route('/user/register/pro', methods=['POST'])
    def new_professional():
        try:
            body = dict(request.form)
            if(body["email"] == ""):
                return jsonify({"msg":"correo no es valido"}),404
            if(body["user_name"] == ""):
                return jsonify({"msg":"usuario no es valido"}),404
            if(body["password"] == ""):
                return jsonify({"msg": "escribe una contraseña"}),404
            if(body["phone"] == ""):
                return jsonify({"msg":"numero no es valido"}),404
            if(body["location"]== ""):
                return jsonify({"msg":"localidad no es alida"}),404
            if(body["direction"] == ""):
                return jsonify({"msg":"direccion no es valida"}),404
            if(len(request.files)!=0): #explicacion de esta linea
                f = request.files['avatar']
                img_url=save_image(f)
            else:
                img_url = "https://res.cloudinary.com/dyfwsdqx8/image/upload/v1615318577/default_avatar_pro_sreecc.png"
            email_check= db.session.query(Userpro).filter(Userpro.email==body['email']).first()
            user_check= db.session.query(Userpro).filter(Userpro.user_name==body['user_name']).first()
            if email_check is None and user_check is None:
                encrypt_pass = encrypted_pass(body["password"]) 
                new_user = Userpro(user_name=body['user_name'],password=encrypt_pass, email=body['email'],phone=body['phone'],url=body['url'],location=body['location'],direction=body['direction'],vat_number=body['vat_number'],social_reason=body['social_reason'],avatar=img_url)
                db.session.add(new_user) #sin este linea no se añade a la base de datos
                db.session.commit()
                response_body = {
                    "msg": new_user.serialize()
                }
                return jsonify(response_body),201
            else:
                return jsonify("Correo o nombre de usuario ya existen"),409
        except OSError as error:
            return jsonify("Error"), 400
        except KeyError as error:
            return jsonify("Error Key" + str(error)),400


    @app.route('/user/pro', methods=['GET'])
    def all_proffesionals():
        body = Userpro.query.all()
        list_pro = []
        for user in body:
            list_pro.append(user.serialize())
        return jsonify(list_pro),200

    @app.route('/pro',methods=['GET'])
    @token_required
    def get_pro(user):
        #body = request.get_json()
        user_pro = Userpro.query.filter_by(id=user["id"]).first()
        if user_pro is not None:
            return jsonify(user_pro.serialize()),200 
        else:
            return jsonify("usuario no existe"),400

    @app.route("/pro",methods=["PUT"])
    @token_required
    def edit_account_pro(user):
        body =dict(request.form) #el body es dict por que viene una foto como hice con el registro como hay foto que se viene hay que ponerlo en dict(reques.form) 
        if request.files:
            f = request.files['avatar']
            img_url = save_image(f)
            body["avatar"] = img_url
        user_pro = Userpro.query.filter_by(id=user["id"]).first() #es donde estan los dato antiguos
        if user_pro is not None: 
            for key in body: #el key es la propiedad que voy a cambiar
                setattr(user_pro,key,body[key]) #setattr le estoy diciendo que entre a user_pro
            db.session.commit()
        
            return jsonify(user_pro.serialize()), 200
        else:
            return jsonify("usuario no existe"),400


    