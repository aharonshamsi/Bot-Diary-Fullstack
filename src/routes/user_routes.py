from flask import request, jsonify
from app import app
from src.services.user_service import create_user
from src.services.user_service import execute_deletion



#===============================================================
@app.route("/user", methods = ['POST'])
def add_user():
    data = request.json

    if not data or not 'username' in data or \
        not 'email' in data or not 'password_hash' in data:
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
def delete_user():
    user_id = request.args.get("user_id")

    if not user_id or not user_id.isdigit():
        return jsonify({"error": "Missing user_id"}), 400
    
    try:
        execute_deletion(user_id)
        return jsonify({"message": "Event deleted successfully!"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
    except Exception as e:
        return jsonify({"error": "Internal server error: " + str(e)}), 500



