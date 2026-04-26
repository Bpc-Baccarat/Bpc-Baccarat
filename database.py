import os
from supabase import create_client, Client

# 請填入您的 Supabase 資訊 (或設定環境變數)
SUPABASE_URL = "https://wbkpffhhupfltgkrjnxv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6India3BmZmhodXBmbHRna3Jqbnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzcyMTMzODUsImV4cCI6MjA5Mjc4OTM4NX0.GvAudGPZyxkS4drgAHV4H18OduabgendHGFtCixhaE0"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def init_db():
    # Supabase 通常透過網頁介面建立 Table
    # 請在 SQL Editor 執行：
    # CREATE TABLE users (user_id bigint PRIMARY KEY, username text, balance float DEFAULT 0);
    # CREATE TABLE transactions (id serial PRIMARY KEY, user_id bigint, amount float, status text);
    pass

async def get_balance(user_id):
    res = supabase.table("users").select("balance").eq("user_id", user_id).execute()
    return res.data[0]['balance'] if res.data else 0.0

async def update_balance(user_id, username, amount):
    # 使用 Upsert 邏輯
    data = {"user_id": user_id, "username": username, "balance": amount}
    # 這裡建議使用 RPC 或先 Select 再 Update 以確保累加正確
    curr = await get_balance(user_id)
    new_bal = curr + amount
    supabase.table("users").upsert({"user_id": user_id, "username": username, "balance": new_bal}).execute()
    return new_bal
