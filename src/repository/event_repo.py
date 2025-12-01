# src/repositories/event_repo.py
from app import db
from sqlalchemy import func 
from src.models.event_model import Event # ייבוא המודל שנוצר


def add_event_by_id(new_event):
    db.session.add(new_event) # עגלת קניות: כלומר מוספים את האירוע אל הגעלת הקניות
    db.session.commit() # אומר לסשן קח את כל מה שיש כעת בעגלת הקניות ושלח למסד נתונים 



def get_event_by_user(user_id: int, specific_date = None) -> bool:

    query = Event.query.filter_by(user_id = user_id)

    if specific_date:
        query = query.filter(func.date(Event.start_time) == specific_date)
    return query.all()



def delete_event_by_ids(event_id: int, user_id: int) -> bool:
    # שאילתה שמוודאת שהאירוע שייך למשתמש (אבטחה)
    event_to_delete = db.session.execute(
        db.select(Event).filter_by(event_id=event_id, user_id=user_id)
    ).scalar_one_or_none()

    if event_to_delete:
        db.session.delete(event_to_delete)
        db.session.commit()
        return True 
    
    return False 



def update_event_by_ids(event_id: int, user_id: int, new_data) -> bool:
    
    event = Event.query.filter_by(event_id = event_id, user_id = user_id).first()

    if event:
        if 'title' in new_data:
            event.title = new_data['title']

        if 'description' in new_data:
            event.description = new_data['description']
        
        if 'start_time' in new_data:
            event.start_time = new_data['start_time']
        
        if 'end_time' in new_data:
            event.end_time = new_data['end_time']

        db.session.commit()
        return True
    
    return False
    
            




