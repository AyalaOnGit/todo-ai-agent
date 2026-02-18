from typing import Optional, List

# רשימה גלובלית שתשמש כ"מסד הנתונים" שלנו
tasks = []
id_counter = 1

def add_task(title: str, description: str = "", task_type: str = "כללי", 
             start_date: str = None, end_date: str = None):
    global id_counter
    new_task = {
        "id": id_counter,
        "title": title,
        "description": description,
        "type": task_type,
        "start_date": start_date,
        "end_date": end_date,
        "status": "פתוח"
    }
    tasks.append(new_task)
    id_counter += 1
    return f"משימה חדשה נוצרה: {title} (קוד: {new_task['id']})"

def get_tasks(status: Optional[str] = None):
    if status:
        return [t for t in tasks if t['status'] == status]
    return tasks

def update_task(title: str, new_status: str):  # שימי לב לשם new_status
    global tasks
    for task in tasks:
        if task["title"] == title:
            task["status"] = new_status
            return f"הסטטוס של המשימה '{title}' עודכן ל-{new_status}."
    return f"לא נמצאה משימה בשם '{title}'."

def delete_task(title: str):
    global tasks
    initial_length = len(tasks)
    # שומרים רק את המשימות שהכותרת שלהן לא שווה למה שביקשנו למחוק
    tasks = [t for t in tasks if t["title"] != title]
    
    if len(tasks) < initial_length:
        return f"המשימה '{title}' נמחקה בהצלחה!"
    else:
        return f"לא נמצאה משימה בשם '{title}'."