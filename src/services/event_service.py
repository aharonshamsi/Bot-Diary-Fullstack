from datetime import datetime
from src.models.event_model import Event
from src.repository.event_repo import delete_event_by_ids
from src.repository.event_repo import get_event_by_user_id
from src.repository.event_repo import add_event_by_id
from src.repository.event_repo import update_event_by_ids


#=====================================================
def create_event(data: Event) -> Event:

    try:
        # Validation 
        user_id_int = int(data['user_id'])
        title_str = str(data['title'])
        start_time_str = str(data['start_time'])

        # שתי שדות אפיונאליים בדיקה שונה, כלומר רק אם יש בהם ערך עשה ולידציה 
        description_str = data.get('description')
        end_time_str = data.get('end_time')

        if description_str is not None:
            end_time_str = str(description_str)
        
        if end_time_str is not None:
            end_time_str = str(end_time_str)

    except ValueError:
        raise ValueError("Invalid user_id format")

    new_event = Event(
    user_id = user_id_int,
    title = title_str,
    start_time = start_time_str,
    description=description_str,
    end_time = end_time_str
    )

    add_event_by_id(new_event)

    return new_event




#=========================================================
def fetch_user_events(user_id: str, date = None) -> None:

    try:
        user_id_int = int(user_id)

    except ValueError:
        return ValueError("Invalid ID format provided.") # 400
    
    if date:
        try:
            validated_date = None
            validated_date = datetime.strptime(date, '%Y-%m-%d').date()

        except ValueError:
            raise ValueError("Invalid date format for filtering. Use YYYY-MM-DD")
    
    events_list = get_event_by_user_id(user_id_int, date)

    # 3. עיבוד לתוצאה לוגית/עסקית – במקרה הזה, המרה למילון
    output = []
    for event in events_list:
        output.append({
            'event_id': event.event_id,
            'title': event.title,
            'start_time': event.start_time.isoformat(),
            'description': event.description,
            'end_time': event.end_time.isoformat() if event.end_time else None
        })

    return output




def execute_deletion(event_id: str, user_id: str) -> None:

    try:
        event_id_int = int(event_id)
        user_id_int = int(user_id)

    except ValueError:
        # מעלים שגיאה גנרית כדי שה-Route יטפל ב-400
        raise ValueError("Invalid ID format provided.") # 400
        
    # 2. קריאה ל-Repository לבצע את המחיקה
    success = delete_event_by_ids(event_id_int, user_id_int)
    
    # 3. טיפול בתוצאה: אם המחסנאי נכשל, מעלים שגיאה מפורטת
    if not success:
        # במקום להחזיר True/False, אנחנו מעלים שגיאה ספציפית
        raise ValueError("Event not found or unauthorized for deletion.")




def execute_update_event(event_id: str, user_id: str, data) -> None:

    try:
        event_id_int = int(event_id)
        user_id_int = int(user_id)

    except ValueError:
        raise ValueError("Invalid ID format provided.")
    
    success = update_event_by_ids(event_id_int, user_id_int, data)

    if not success:
        raise ValueError("Event not found or unauthorized for update.")


