from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from utils.chatbot_utils import chat_with_student

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

@app.get("/")
async def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())
    
@app.post("/chat")
async def chat(student_id: str = Form(...), message: str = Form(...)):
    student_file = f"students/{student_id}.json"

    try:
        response = chat_with_student(student_file, message)
        return JSONResponse({"response": response})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)