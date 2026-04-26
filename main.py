from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import engine, database as db

app = FastAPI()
game = engine.BaccaratEngine()

# 掛載靜態檔案 (放置您的圖片與 JS)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "hash": game.shoe_hash})

@app.post("/bet")
async def place_bet(user_id: int, side: str, amount: float):
    # 處理下注與開獎邏輯
    res = game.play_round()
    return {"result": res, "new_balance": 1000} # 簡化示範
