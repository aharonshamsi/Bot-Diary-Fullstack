from flask import Flask
from flask_cors import CORS 
from flask_sqlalchemy import SQLAlchemy 
from flask_jwt_extended import JWTManager
from config import Config
from datetime import timedelta

# Create the Flask application instance (the engine)
app = Flask(__name__) 

# Enable CORS to allow requests from the Frontend
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# --- Database Setup ---
# URL for Flask to connect to the MySQL Docker container
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI

# Disable tracking to save memory and improve speed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

# --- Auth Setup (JWT) ---
# Secret key to encrypt and secure user tokens
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY

# Set token life/session duration (1 hour)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)


# --- Initialization ---
db = SQLAlchemy(app)   # Initialize Database object
jwt = JWTManager(app)  # Initialize JWT Authentication



# --- Models ---
# Import database structures for Users and Events
from src.models import user_model, event_model

# --- Routes ---
# Register blueprints for API endpoints (Events, Users, Auth, and Bot)
from src.routes import event_routes
from src.routes import user_routes
from src.routes import auth_routes

from src.routes import bot_routes
import src.routes.transcription_routes


@app.route("/")
def home():
    return "Hello, World! This is the Bot-Diary server."


if __name__ == "__main__":
    app.run(debug=True)
