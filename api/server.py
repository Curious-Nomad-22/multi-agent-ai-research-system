from fastapi import FastAPI
from agents.planner import create_plan
from agents.writer import format_report
app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}
