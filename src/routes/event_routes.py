from flask import request, jsonify
from app import app, db
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from src.models.event_model import Event
from src.services.event_service import create_event
from src.services.event_service import fetch_user_events
from src.services.event_service import execute_deletion
from src.services.event_service import execute_update_event


#================================================================================================
#================================================================================================

# ===== openai אצל הבוט עם התממשקות ל endpoint כלשהוגדרו עד עכשיו הם לפני הגדרת endpointכל ה ======
#================================================================================================


#===================== Add event ======================
@app.route("/event", methods=['POST']) # end point
@jwt_required()
def add_event():

    current_user_id = int(get_jwt_identity())
    data = request.json # שומרים את הבקשה שהגיעה 

    if not data or not 'title' in data or not 'start_time' in data:
        return jsonify({"error": "Missing required data"}), 400
    
    try:
        new_event = create_event(current_user_id, data)

        return jsonify({
            "message": "Event added successfully!",
            "event_id": new_event.event_id
        }), 201


    except ValueError as e:  # שגיאת ולידציה
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    


#===================== Get event ======================
@app.route("/event", methods = ['GET'])
@jwt_required()
def get_event():
    current_user_id = int(get_jwt_identity())
    date = request.args.get('date')

    # מיותר אחרי הטוקן, כי אם אין טוקן יוחזר שגיאה 401 ואם הוא תקין תמיד יש בו user_id
    # if not current_user_id:
    #     return jsonify({"error": "Missing user_id parameter in URL"})
    
    try:
        events_output = fetch_user_events(current_user_id, date)
        return jsonify({"events": events_output}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "Internal server error: " + str(e)}), 500




#===================== Delete event ======================
@app.route("/event", methods = ['DELETE'])
@jwt_required()
def delete_event():

    current_user_id = int(get_jwt_identity())
    event_id = request.args.get('event_id')

    if not event_id:
        return jsonify({"error": "Missing event_id"}), 400
    
    try:
        execute_deletion(current_user_id, event_id) 
        return jsonify({"message": "Event deleted successfully!"}), 200

    except ValueError as e:
        # תופס את השגיאה מה-Service ("לא נמצא / אין הרשאה")
        # ומחזיר קוד 404 (Not Found)
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": "Internal server error: " + str(e)}), 500
    



#===================== Update event ======================
@app.route("/event", methods = ['PUT'])
@jwt_required()
def update_event():

    current_event_id = int(get_jwt_identity())
    event_id = request.args.get('event_id')

    # נתונים לשינוי
    data = request.json

    if not event_id:
        return jsonify({"error": "Missing event_id"}), 400
    
    if not data:
        return jsonify({"error": "No data provided for update"}), 400
    
    try:
        execute_update_event(current_event_id, event_id, data)
        return jsonify({"message": "Event update successfully!"}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": "Internal server error: " + str(e)}), 500

    
