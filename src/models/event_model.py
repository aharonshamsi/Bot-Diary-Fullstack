from app import db

class Event(db.Model):
    __tablename__ = 'events'  # שם הטבלה ב-MySQL
    
    event_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


    