from flask import request, jsonify
from app import app
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from src.functions.event_function import get_events_function
from src.services.event_service import execute_update_event, execute_deletion

import json
from openai import OpenAI
from src.functions import FUNCTION_DEFINITIONS, FUNCTION_MAP

from config import Config

api_key = Config.API_KEY
client = OpenAI(api_key=api_key)


@app.route("/bot", methods=["GET", "POST", "DELETE"])
@jwt_required()
def bot_chat():
    current_user_id = int(get_jwt_identity())
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "Missing message"}), 400

    # Sending the first request for the model
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

    # Check if was function calling
    if message.function_call:

        print(message.function_call.name)
        print(message.function_call.arguments)

        function_name = message.function_call.name
        args = json.loads(message.function_call.arguments) # Creating dict

        function_to_call = FUNCTION_MAP[function_name]

        # Calling a function that does not exist in the function array
        if not function_to_call:
            return jsonify({"reply": f"Unknown function: {function_name}"}), 400


        # ===========  Delete or Update =======================
        if function_name in ("delete_event", "update_event"):

            all_events = get_events_function(current_user_id)
            print(function_name)

            system_prompt = (
                "You are an assistant that resolves user intent on calendar events.\n"
                "Return ONLY valid JSON.\n"
            )

            # Description for Delete
            if function_name == "delete_event":
                system_prompt += (
                    "Select the event to delete.\n"
                    "Format: {\"event_id\": 42}"
                )

            # Description for Update
            elif function_name == "update_event":
                system_prompt += (
                    "Select the event to update and extract only changed fields.\n"
                    "Format: {\"event_id\": 42, \"data\": {...}}"
                )


            # Function call Delete or Update
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                    {
                        "role": "assistant",
                        "content": f"User events:\n{json.dumps(all_events, ensure_ascii=False)}"
                    }
                ]
            )


            # Sending the model response to the treatment of function
            content = response.choices[0].message.content

            try:

                payload = json.loads(content) # Create a dict from the model's response
                event_id = payload["event_id"]
                data = payload.get("data", {})

            except Exception:
                return jsonify({"reply": "לא הצלחתי לזהות את האירוע"}), 200

            if function_name == "delete_event":
                result = function_to_call (user_id=current_user_id, event_id=event_id)
                reply = f"האירוע נמחק בהצלחה (ID: {event_id})"

            elif function_name == "update_event":
                result = function_to_call(user_id=current_user_id, event_id=event_id, data=data)
                reply = f"האירוע עודכן בהצלחה (ID: {event_id})"

            return jsonify({"reply": reply}), 200
        



        # ================== Get event ==================
        elif function_name == "get_events":
            result = function_to_call(user_id=current_user_id, **args)

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
        
    

        # ================== Add event ==================
        elif function_name == "add_event":
            result = function_to_call(user_id=current_user_id, **args)
            reply = f"האירוע נוסף בהצלחה: {result.get('title', 'ללא כותרת')}"
            return jsonify({"reply": reply}), 200
        
        

    # ================== No function called ==================
    return jsonify({"reply": "לא זוהתה פעולה לביצוע"}), 200

    
