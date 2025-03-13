import BackEnd.GlobalInfo.ResponseMessages as ResponseMessage
import BackEnd.GlobalInfo.Keys as Colabskey
from pymongo import MongoClient
from flask import jsonify

# Conexión a MongoDB Atlas
if Colabskey.dbconn is None:
    mongoConnect = MongoClient(Colabskey.strConnection)
    Colabskey.dbconn = mongoConnect[Colabskey.strDBConnection]


dbUsuario = Colabskey.dbconn["usuario"]
dbValvula = Colabskey.dbconn["valvula"]



def fnAuthPost(usuario, password):
    try:
        # Lógica para verificar si el usuario y contraseña existen en la base de datos
        objQuery = dbUsuario.find_one({"nombre": usuario, "contraseña": password})
        print("Resultado de la consulta:", objQuery)
        if objQuery:
            return jsonify({"Acreditado": True, "mensaje": "Inicio de sesión exitoso"})
        else:
            return jsonify({"Acreditado": False, "mensaje": "Usuario o contraseña incorrectos"})
    except Exception as e:
        print("Error en fnAuthPost:", e)
        return jsonify({"Acreditado": False, "mensaje": "Error en el servidor"})

#nuevo usuario
def fnRegisterUser(usuario, password):
    try:
        print(f"Registrando nuevo usuario: {usuario}")

        # Verificar si el usuario ya existe
        if dbUsuario.find_one({"nombre": usuario}):
            return jsonify({"mensaje": "El usuario ya existe", "success": False})

        # Insertar nuevo usuario
        new_user = {"nombre": usuario, "contraseña": password}
        dbUsuario.insert_one(new_user)

        return jsonify({"mensaje": "Usuario registrado correctamente", "success": True})

    except Exception as e:
        print("Error al registrar usuario:", e)
        return jsonify({"mensaje": "Error en el servidor", "success": False})
    
#valvula
def programar_riego(abrir, cerrar, dias):
    try:
        # Verifica que se reciban datos válidos
        if not abrir or not cerrar or not dias:
            return {"mensaje": "Por favor, complete todos los campos.", "success": False}

        # Estructura de datos para la base de datos
        riego_data = {
            "abrir": abrir,        # Hora de apertura
            "cerrar": cerrar,      # Hora de cierre
            "dias": dias           # Lista de días seleccionados (por ejemplo, ['lunes', 'miercoles', 'viernes'])
        }

        # Guardar los datos en la base de datos
        result = dbValvula.insert_one(riego_data)

        if result.inserted_id:
            return {"mensaje": "Riego programado exitosamente", "success": True}
        else:
            return {"mensaje": "Error al programar el riego", "success": False}

    except Exception as e:
        print("Error al programar el riego:", e)
        return {"mensaje": "Error al guardar los datos en la base de datos", "error": str(e), "success": False}