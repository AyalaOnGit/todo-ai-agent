
import os
from dotenv import load_dotenv
import json
import httpx
from groq import Groq
from todo_service import add_task, get_tasks, update_task, delete_task

load_dotenv()

# 1. יוצרים לקוח HTTP מיוחד שמתעלם מהאימות של נטפרי
http_client = httpx.Client(verify=False)

#2 שליפת המפתח מה-env תוך שמירה על ה-http_client שעוקף את ה-SSL
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    http_client=http_client
)




# הגדרת הכלים (Tools) עבור המודל
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "הוספת משימה חדשה לרשימה",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "כותרת המשימה"},
                    "task_type": {"type": "string", "description": "סוג המשימה (לימודים, עבודה, בית)"},
                    "end_date": {"type": "string", "description": "תאריך סיום"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "קבלת רשימת המשימות הקיימות",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "עדכון סטטוס של משימה קיימת (למשל סימון כבוצע)",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "כותרת המשימה המדויקת"},
                    "new_status": {
                        "type": "string", 
                        "enum": ["open", "done"], 
                        "description": "הסטטוס החדש: 'done' לסימון כבוצע או 'open' לפתיחה מחדש"
                    }
                },
                "required": ["title", "new_status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "מחיקת משימה מהרשימה לפי הכותרת שלה",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "כותרת המשימה שרוצים למחוק"}
                },
                "required": ["title"]
            }
        }
    }
]

def agent(query: str):
    # פנייה ראשונה ל-Groq כדי להבין את הכוונה
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # מודל חזק ומהיר של מטא שרץ על Groq
        messages=[
                # הוספת שורת סיסטם שגורמת לו להבין שהוא עוזר אישי
                {"role": "system", "content": "אתה עוזר אישי לניהול משימות. אם המשתמש מבקש למחוק, לעדכן או להוסיף - השתמש בכלים המתאימים."},
                {"role": "user", "content": query}
            ],
        tools=tools,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # אם המודל החליט להפעיל פונקציה
    if tool_calls:
        available_functions = {
            "add_task": add_task,
            "get_tasks": get_tasks,
            "update_task": update_task,
            "delete_task": delete_task, # להוסיף את זה כאן
        }
        
        # הרצת הפונקציה
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            
            # ביצוע הפעולה ב-todo_service
            if function_args:
                function_response = function_to_call(**function_args)
            else:
                function_response = function_to_call()
            
            # החזרת התוצאה ל-Groq כדי שינסח תשובה סופית
            final_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": query},
                    response_message,
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(function_response),
                    }
                ]
            )
            return final_response.choices[0].message.content

    return response_message.content