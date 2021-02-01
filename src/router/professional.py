from flask import request,jsonify

def professional_route(app,token_required):

    @app.route('/user/register/pro', methods=['POST'])
    def new_proffesional():
        body = request.get_json()
        new_user = Userpro(user_name=body['user_name'], email=body['email'],password=body['password'],phone=body['phone'],url=body['url'],location=body['location'],direction=body['direction'],vat_number=body['vat_number'],social_reason=body['social_reason'])
        db.session.add(new_user) #sin este linea no se añade a la base de datos
        db.session.commit() # esta es la hermana de la que esta arriba :) 
        print(new_user.serialize())
        return jsonify(new_user.serialize()),200

    @app.route('/user/pro', methods=['GET'])
    def all_proffesionals():
        body = Userpro.query.all()
        for x in body:
            print(x.serialize())
        print(body)

    @app.route('/pro/<int:id>',methods=['GET'])
    def get_pro(id):
        user_pro_by_id = Userpro.query.filter_by(id=id).filter_by(is_active=False).first()
        print(user_pro_by_id)
        if user_pro_by_id is not None:
            return jsonify(user_pro_by_id.serialize()), 200
        else:
            return jsonify("usuario no existe"),400