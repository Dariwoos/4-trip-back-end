import os
from os.path import join
from flask import request,jsonify
from models import db,Userpro
from encrypted import encrypted_pass
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import base64

host = "vhttps://3000-d6620844-473e-4005-a216-c78a8882d46d.ws-eu03.gitpod.io/"

def professional_route(app,token_required):

    @app.route('/user/register/pro', methods=['POST'])
    def new_professional():
        try:
            body = dict(request.form)
            print(body)
            if(body["email"] == ""):
                return jsonify({"msg":"correo no es valido"}),400
            if(body["user_name"] == ""):
                return jsonify({"msg":"usuario no es valido"}),400
            if(body["password"] == ""):
                return jsonify({"msg": "escribe una contraseña"}),400
            if(body["phone"] == ""):
                return jsonify({"msg":"numero no es valido"}),400
            if(body["location"]== ""):
                return jsonify({"msg":"localidad no es alida"}),400
            if(body["direction"] == ""):
                return jsonify({"msg":"direccion no es valida"}),
                
            print(request.file,"strien@@@gggggggggghggggggggGGGGGGGGGG")

            f = request.files['avatar']
            filename= secure_filename(f.filename)
            f.save(os.path.join("./src/img",filename))
            img_url = host+filename
            new_user = Userpro(user_name=body['user_name'],password=body["password"], email=body['email'],phone=body['phone'],url=body['url'],location=body['location'],direction=body['direction'],vat_number=body['vat_number'],social_reason=body['social_reason'],avatar=img_url)
            encrypt_pass = encrypted_pass(body["password"]) 
            print(new_user.serialize(),"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            db.session.add(new_user) #sin este linea no se añade a la base de datos
            db.session.commit()
            print(new_user.serialize())
            response_body = {
                "msg": new_user.serialize()
            }
            return jsonify(response_body),201
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
        body = request.get_json()
        user_pro = Userpro.query.filter_by(id=user["id"]).first()
        print(user_pro)
        if user_pro is not None:
            return jsonify(user_pro.serialize()),200 
        else:
            return jsonify("usuario no existe"),400

    @app.route("/pro",methods=["PUT"])
    @token_required
    def edit_account_pro(user):
        body = request.get_json() #aqui es el body que quiero cambiar   
        user_pro = Userpro.query.filter_by(id=user["user"]).first() #es donde estan los dato antiguos
        if user_pro is not None: 
            for key in body: #el key es la propiedad que voy a cambiar
                print('key',key)
                setattr(user_pro,key,body[key]) #setattr le estoy diciendo que entre a user_pro
            db.session.commit()
            return jsonify(user_pro.serialize()), 200
        else:
            return jsonify("usuario no existe"),400