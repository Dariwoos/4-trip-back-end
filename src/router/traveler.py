from flask import request,jsonify
from models import db, Traveler

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
            f = request.files["image"]
            new_user = Traveler(username=body["username"],email=body["email"],password=body["password"],avatar=body["avatar"])
            db.session.add(new_user)
            db.session.commit()
            print(new_user.serialize())
            return jsonify("todo bien"), 200
        except OSError as error:
            return jsonify("Error"), 400
        except KeyError as error:
            return jsonify("Error Key" + str(error)),400

