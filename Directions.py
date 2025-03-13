from flask import Flask, jsonify, request 
from flask_cors import CORS, cross_origin
from BackEnd import Functions as CallMethod
import BackEnd.GlobalInfo.ResponseMessages as ResponseMessages


app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"*"}})

@app.route("/mensaje", methods = ["GET"])
@cross_origin(allow_headers=["Content-Type"])
def mensaje():
    try:
        objResult = {"mensaje": "hola que hace?"}
        return objResult
    except Exception as e:
        objResult = {"mensaje": e}
        print("No jalo mijo", e)
        return jsonify(ResponseMessages.err500)
    
#registro
@app.route('/register', methods=['POST'])
@cross_origin(allow_headers=["Content-Type"])
def register():
    try:
        # Obtener datos del JSON
        data = request.json
        usuario = data.get("user")
        password = data.get("pass")

        # Llamar a la función que registra el usuario en la base de datos
        result = CallMethod.fnRegisterUser(usuario, password)

        return result

    except Exception as e:
        print("Error en el registro de usuario:", e)
        return jsonify({"mensaje": "Error en el servidor", "success": False})

#login
@app.route('/logueo',methods=['POST'])
@cross_origin(allow_headers=["Content-Type"])
def logueo():
    try:
        usuario=request.json['user']
        password=request.json['pass']
        ObjResult=CallMethod.fnAuthPost(usuario, password)
        return ObjResult
    except Exception as e:
        print("Error en logueo", e)
        return jsonify(ResponseMessages.err500)
    

#programar_riego
@app.route('/programar_riego', methods=['POST'])
@cross_origin(allow_headers=["Content-Type"])
def programar_riego():
    try:
        # Obtener los datos del request JSON
        data = request.json
        abrir = data['abrir']  # Hora de apertura
        cerrar = data['cerrar']  # Hora de cierre
        dias = data['dias']  # Días seleccionados para el riego

        # Llamar a la función que procesa y guarda los datos en la base de datos
        result = CallMethod.programar_riego(abrir, cerrar, dias)

        return jsonify(result)

    except Exception as e:
        print("Error en programar_riego:", e)
        return jsonify({"mensaje": "Error al programar el riego", "error": str(e)})



""" if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)    """


