from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import engine, database as db

app = FastAPI()

# 遊戲引擎實例化
game = engine.BaccaratEngine()

# 掛載靜態檔案
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 定義下注請求的格式 (防止 POST 錯誤)
class BetRequest(BaseModel):
    side: str
    amount: float

@app.get("/")
async def index(request: Request):
    # 這裡確保參數寫法符合新版 Starlette
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"hash": game.shoe_hash}
    )

@app.post("/bet")
async def place_bet(bet_data: BetRequest):
    try:
        # 1. 執行遊戲邏輯
        result = game.play_round() # 假設這會回傳 'B', 'P', 或 'T'
        
        # 2. 這裡之後對接您的資料庫邏輯
        # 假設扣款成功後的餘額
        new_balance = 10000.0 - bet_data.amount 
        
        # 回傳給前端
        return {
            "success": True,
            "result": result,
            "new_balance": new_balance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
