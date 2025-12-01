from flask import request, jsonify
from app import app
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity


from src.services.user_service import create_user
from src.services.user_service import execute_deletion
from src.services.user_service import execute_update




#===============================================================
@app.route("/user", methods = ['POST'])
def add_user():
    data = request.json

    if not data or not 'username' in data or \
        not 'email' in data or not 'password' in data:
        return jsonify({"error": "Missing required data" }), 400
    
    try:
        new_user = create_user(data)

        return jsonify ({
            'message': "User added successfully!",
            'user_id': new_user.user_id
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": "Internal server error " + str(e)}), 500
    




#===============================================================
@app.route("/user", methods = ['DELETE'])
@jwt_required()
def delete_user():

    current_user_id = get_jwt_identity()
    
    try:
        execute_deletion(current_user_id)
        return jsonify({"message": "Event deleted successfully!"}), 204

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": "Internal server error: " + str(e)}), 500
    



#===============================================================
@app.route("/user", methods = ['PUT'])
@jwt_required()
def update_user():

    current_user_id = int(get_jwt_identity())

    data = request.json 

    # if not user_id:
    #     return jsonify({"error": "Missing user_id"}), 400
    
    if not data:
        return jsonify({"error": "No data provided for update"}), 400
    
    try:
        execute_update(current_user_id, data)
        return jsonify({"message": "User update successfully!"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
    except Exception as e:
        return jsonify({"error": "Internal server error: " + str(e)}), 500









    

        




