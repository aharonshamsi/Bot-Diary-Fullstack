from flask import request, jsonify
from app import app
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

import json
from openai import OpenAI
from src.functions import FUNCTION_DEFINITIONS, FUNCTION_MAP

from config import Config

api_key = Config.API_KEY
client = OpenAI(api_key=api_key)


@app.route("/bot", methods=["GET", "POST"])
@jwt_required()
def bot_chat():
    current_user_id = int(get_jwt_identity())
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "Missing message"}), 400


    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a personal daily diary assistant."
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        functions=FUNCTION_DEFINITIONS,
        function_call="auto"
    )


    message = response.choices[0].message
    


    if message.function_call:
        function_name = message.function_call.name
        args = json.loads(message.function_call.arguments) # Creating dict

        print(message.function_call.arguments) # Check

        if function_name not in FUNCTION_MAP:
            return jsonify({"error": "Unknown function"}), 400


        function_to_call = FUNCTION_MAP[function_name]

        result = function_to_call(
            user_id=current_user_id,
            **args
        )

        # קריאה שניה למודל
        second_response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a personal daily diary assistant."
                },
                {
                    "role": "user",
                    "content": user_message
                },
                {
                    "role": "assistant",
                    "function_call": {
                        "name": function_name,
                        "arguments": message.function_call.arguments
                    }
                },
                {
                    "role": "function",
                    "name": function_name,
                    "content": json.dumps(result)
                }
            ]
        )


        final_message = second_response.choices[0].message.content

        return jsonify({
            "reply": final_message
        }), 200


    return jsonify({
    "reply": message.content
    }), 200



    
