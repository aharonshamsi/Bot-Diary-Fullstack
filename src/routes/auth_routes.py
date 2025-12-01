from app import app
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from src.services.auth_service import authenticate_user


@app.route("/login", methods = ["POST"])
def login():
    
    data = request.json

    if not data or not "username" in data or not "password" in data:
        return jsonify({"error": "Missing username or password"}), 400
    
    try:

        user = authenticate_user(data["username"], data["password"])
        
        # Create JWT for the user
        token = create_access_token(identity=str(user.user_id))
        

        return jsonify({
        "message": "Login successful",
        "access_token": token
    }), 200


    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": "Internal server error " + str(e)}), 500
    




