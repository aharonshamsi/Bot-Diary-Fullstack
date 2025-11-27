from app import db

class User(db.Model):
    __tablename__ = 'users'  # users שם הטבלה כלומר תחבר את המודל הזה לטבלה שנקראת -MySQL
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())