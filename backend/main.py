from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware # ייבוא לצורך אישור גישה מה-React
from agent_service import agent
from todo_service import get_tasks # ודאי שיש לך את ה-import הזה

# הגדרת האפליקציה עם כותרת
app = FastAPI(title="Todo Agent API")

# הגדרת Middleware של CORS - מאפשר ל-React (שבתדר 3000) לדבר עם ה-FastAPI (שבתדר 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # מאפשר גישה מכל מקור (לצורכי פיתוח)
    allow_credentials=True,
    allow_methods=["*"], # מאפשר את כל סוגי הבקשות (GET, POST וכו')
    allow_headers=["*"], # מאפשר את כל סוגי ה-Headers
)

# הגדרת המבנה של ההודעה שמגיעה מהמשתמש (Pydantic Model)
class ChatRequest(BaseModel):
    message: str

# נקודת בדיקה בסיסית - לוודא שהשרת רץ
@app.get("/")
def read_root():
    return {"status": "The Todo Agent is online!"}

# נתיב שמציג את כל המשימות השמורות בזיכרון
@app.get("/tasks")
def show_all_tasks():
    """נתיב שמציג את כל המשימות השמורות בזיכרון"""
    return {"all_tasks": get_tasks()}

# הנתיב המרכזי לשיחה עם ה-Agent
@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    """שליחת ההודעה ל-Agent וקבלת תשובה"""
    # שליחת ההודעה ל-Agent וקבלת תשובה מהמוח של ה-AI
    response = agent(request.message)
    return {"reply": response}