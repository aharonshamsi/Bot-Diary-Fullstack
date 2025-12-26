from datetime import datetime
from src.models.event_model import Event
from src.repository.event_repo import delete_event_by_ids
from src.repository.event_repo import get_event_by_user
from src.repository.event_repo import add_event_by_id
from src.repository.event_repo import update_event_by_ids


import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


#=====================================================
def create_event(current_user_id: int, data: Event) -> None:

    try:
        # Validation 
        title_str = str(data['title'])
        start_time_str = str(data['start_time'])

        # שתי שדות אפיונאליים בדיקה שונה, כלומר רק אם יש בהם ערך עשה ולידציה 
        description_str = data.get('description')
        end_time_str = data.get('end_time')

        if description_str is not None:
            description_str = str(description_str)
        
        if end_time_str is not None:
            end_time_str = str(end_time_str)

        # validate start_time הוא זמן תקין
        start_time_dt = datetime.fromisoformat(start_time_str)
        

    except ValueError:
        raise ValueError("Invalid event data format")

    new_event = Event(
    user_id = current_user_id,
    title = title_str,
    start_time = start_time_dt,
    description=description_str,
    end_time = end_time_str
    )

    add_event_by_id(new_event)
    # return new_event

    # function callהמרה לגייסון בשביל ה 
    new_event_json = {
        "user_id": new_event.user_id,
        "title": new_event.title,
        "start_time": new_event.start_time.isoformat(),  # הפוך ל-string
        "description": new_event.description,
        "end_time": new_event.end_time.isoformat() if new_event.end_time else None
    }

    return new_event_json



# מחלץ שעה ותאריך ממה שחזר מהמודל
def resolve_time_extended(time_reference: str) -> datetime:
    now = datetime.utcnow()
    time_reference = time_reference.lower().strip()
    
    # שעות ודקות
    hour_match = re.search(r"(\d{1,2}):(\d{2})", time_reference)
    if hour_match:
        hour = int(hour_match.group(1))
        minute = int(hour_match.group(2))
    else:
        hour = 0
        minute = 0
    
    # ימים / שבועות / חודשים
    day_match = re.search(r"(\d+)\s*day", time_reference)
    if day_match:
        days = int(day_match.group(1))
        return (now + relativedelta(days=days, hour=hour, minute=minute, second=0, microsecond=0))
    
    week_match = re.search(r"(\d+)\s*week", time_reference)
    if week_match:
        weeks = int(week_match.group(1))
        return (now + relativedelta(weeks=weeks, hour=hour, minute=minute, second=0, microsecond=0))
    
    if "month" in time_reference:
        return (now + relativedelta(months=1, hour=hour, minute=minute, second=0, microsecond=0))
    
    if "tomorrow" in time_reference:
        return (now + relativedelta(days=1, hour=hour, minute=minute, second=0, microsecond=0))

    # ברירת מחדל
    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)





#=========================================================
def fetch_user_events(user_id: str, date = None) -> None:

    try:
        user_id_int = int(user_id)

    except ValueError:
        raise ValueError("Invalid ID format provided.")
    
    if date:
        try:
            validated_date = None
            validated_date = datetime.strptime(date, '%Y-%m-%d').date()

        except ValueError:
            raise ValueError("Invalid date format for filtering. Use YYYY-MM-DD")
    
    events_list = get_event_by_user(user_id_int, date)

    # 3. עיבוד לתוצאה לוגית/עסקית – במקרה הזה, המרה למילון
    output_events = []
    for event in events_list:
        output_events.append({
            'event_id': event.event_id,
            'title': event.title,
            'start_time': event.start_time.isoformat(),
            'description': event.description,
            'end_time': event.end_time.isoformat() if event.end_time else None
        })

    return output_events




def execute_deletion(current_user_id: int, event_id: str) -> None:

    try:
        event_id_int = int(event_id)

    except ValueError:
        # מעלים שגיאה גנרית כדי שה-Route יטפל ב-400
        raise ValueError("Invalid ID format provided.") # 400
        
    # 2. קריאה ל-Repository לבצע את המחיקה
    success = delete_event_by_ids(current_user_id, event_id_int)
    
    # 3. טיפול בתוצאה: אם המחסנאי נכשל, מעלים שגיאה מפורטת
    if not success:
        # במקום להחזיר True/False, אנחנו מעלים שגיאה ספציפית
        raise ValueError("Event not found or unauthorized for deletion.")




def execute_update_event(current_event_id: int, event_id: str, data: dict) -> None:

    try:
        event_id_int = int(event_id)

        valid_data = {} # Create dictionary

        if 'title' in data:
            valid_data['title'] = str(data['title'])

        if 'description' in data:
            valid_data['description'] = str(data['description'])
        
        if 'start_time' in data:
            valid_data['start_time'] = str(data['start_time'])

        if 'end_time' in data:
            valid_data['end_time'] = str(data['end_time'])

            
    except ValueError:
        raise ValueError("Invalid ID format provided.")
    
    success = update_event_by_ids(current_event_id, event_id_int, valid_data)

    if not success:
        raise ValueError("Event not found or unauthorized for update.")


