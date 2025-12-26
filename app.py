from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_jwt_extended import JWTManager
from config import Config
from datetime import timedelta

app = Flask(__name__) #  אוביקט שמחזיק את האפליקציה כלומר מנוע של היישום 


# MySQL שורת החיבור של השרת אל מסד הנתונים 
# app.config זה config פנימי של Flask
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI

# האוביקט עוכב אחר הזיכרון ושולח אותות, זה הרבה משאבים ולכן כיבנו אותו 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

# המפתח הזה הוא הכלי שספריית JWT (JSON Web Token) משתמשת בו כדי להצפין את ה"דרכון" של המשתמש.
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1) # זמן חיבור הטוקן הוא שעה



db = SQLAlchemy(app)  #  אתחול אובייקט מסד הנתונים
jwt = JWTManager(app) # חיבור הספריה לאפליקציה, כדי שתוכל לייצר טוקנים חדשים לאחר הlogin


from src.models import user_model, event_model

from src.routes import event_routes
from src.routes import user_routes
from src.routes import auth_routes

# Bot
from src.routes import bot_routes


@app.route("/")
def home():
    return "Hello, World! This is the Bot-Diary server."


if __name__ == "__main__":
    app.run(debug=True)
