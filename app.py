from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
import config

app = Flask(__name__) #  אוביקט שמחזיק את האפליקציה כלומר מנוע של היישום 


# MySQL שורת החיבור של השרת אל מסד הנתונים 
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
# האוביקט עוכב אחר הזיכרון ושולח אותות, זה הרבה משאבים ולכן כיבנו אותו 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)  #  אתחול אובייקט מסד הנתונים

from src.models import user_model, event_model

from src.routes import event_routes
from src.routes import user_routes


@app.route("/")
def home():
    return "Hello, World! This is the Bot-Diary server."


if __name__ == "__main__":
    app.run(debug=True)







# # --- כאן מתחיל המודל ---
# class User(db.Model):
#     __tablename__ = 'users'  # users שם הטבלה כלומר תחבר את המודל הזה לטבלה שנקראת -MySQL
    
#     user_id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())



# --- כאן מתחיל מודל האירועים 
# class Event(db.Model):
#     __tablename__ = 'events'  # שם הטבלה ב-MySQL
    
#     event_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     title = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     start_time = db.Column(db.DateTime, nullable=False)
#     end_time = db.Column(db.DateTime, nullable=True)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())





# @app.route("/")
# def home():
#     return "Hello, World! This is the Bot-Diary server."


# # This is endpoint to add new event to the database
# @app.route("/event", methods=['POST']) # יצירת נקודת קצה כלומר נתיב ספיציפי בAPI 
# def add_event(): # פונקציה להוספת אירוע 
#     data = request.json # שומרים את הבקשה שהגיעה 

#     if not data or not 'user_id' in data or not 'title' in data or not 'start_time' in data:
#         return jsonify({"error": "Missing required data"}), 400
    
#     try:
        
#         new_event = Event(
#             user_id = data['user_id'],
#             title = data['title'],
#             start_time = data['start_time'],
#             description=data.get('description'),
#             end_time = data.get('end_time')
#             )
        
#         db.session.add(new_event) # עגלת קניות: כלומר מוספים את האירוע אל הגעלת הקניות

#         db.session.commit() # אומר לסשן קח את כל מה שיש כעת בעגלת הקניות ושלח למסד נתונים 

#         return jsonify({"message": "Event added successfully!", "event_id": new_event.event_id}), 201

#     except Exception as e:
#         db.session.rollback() # היה כשל ולכן תזרוק את כל מה שיש בעגלה לפח
#         return jsonify({"error":str(e)}), 500
    


# # This is
# @app.route("/get", methods = ['GET'])
# def get_event():
#     user_id = request.args.get('user_id') # מילון שמכיל את כל הפרמטרים שאחרי הסימן ? שבכתובת הבקשה, המפתח הוא user_id והערך שלו הוא למשל 1 
    
#     if not user_id:
#         return jsonify({"error": "Missing user_id parameter in URL"})
    
#     # פה ננסה לבצע את השאילתה למסד נתונים
#     try:
#         # SQL: SELECT * FROM events WHERE user_id
#         # all() אוסף את כל התוצאות לאוביקט מטיפוס Event
#         events_list = Event.query.filter_by(user_id = user_id).all() 

#         # לאחר שמצאנו את כל האירועים של המשתמש הזה, הם קיימים באובייקט של פייתון ולכן נבצע המרה למילון json
#         output = []
#         for event in events_list:
#             event_data = {
#                 'event_id': event.event_id,
#                 'title': event.title,
#                 'start_time': event.start_time.isoformat(),
#                 'description': event.description,
#                 'end_time': event.end_time.isoformat() if event.end_time else None
#             }
#             output.append(event_data) # הוספה של המילון event_data אל הרשימה שנקאת output

#         return jsonify({"events": output}), 200
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500




# @app.route("/event", methods = ['DELETE'])
# def delete_event():

#     event_id = request.args.get('event_id')
#     user_id = request.args.get('user_id')

#     if not event_id or not user_id:
#         return jsonify({"error": "Missing event_id or user_id"}), 400
    
#     try:
#         event_to_delete = Event.query.filter_by(event_id = event_id, user_id = user_id).first()

#         if not event_to_delete:
#             return jsonify({"error": "Event ont found or does not belong to this user"}), 404
        
#         db.session.delete(event_to_delete) # סימון למחיקה
#         db.session.commit()

#         return jsonify({"message": "Event deleted successfully!"}), 200


#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500




